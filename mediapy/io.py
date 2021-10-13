import json
import logging
import os.path
import platform
import subprocess as sp
import sys
import threading
from typing import Optional, Dict, List, Tuple, IO, Union

import numpy as np
from pydantic import BaseModel

"""
https://www.ffmpeg.org/documentation.html
"""

logger = logging.getLogger("mediapy")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
good_format = logging.Formatter('%(asctime)s pid=%(process)d %(filename)s:%(lineno)s %(funcName)s [%(name)s]-%(levelname)s: %(message)s')
handler.setFormatter(good_format)
logger.addHandler(handler)


def _ffmpeg_common(options, show_log: bool):
    if not show_log:
        options.extend(["-hide_banner", "-loglevel", "error"])


class VideoStreamMeta(BaseModel):
    # 视频数据元信息
    index: int
    codec_name: str
    codec_long_name: str
    profile: Optional[str]
    codec_type: str
    codec_tag_string: str
    codec_tag: str
    width: int
    height: int
    coded_width: int
    coded_height: int
    closed_captions: int
    film_grain: int
    has_b_frames: int
    sample_aspect_ratio: str
    display_aspect_ratio: str
    pix_fmt: str
    level: int
    color_range: Optional[str]
    color_space: Optional[str]
    color_transfer: Optional[str]
    color_primaries: Optional[str]
    chroma_location: Optional[str]
    field_order: Optional[str]
    is_avc: Optional[str]
    r_frame_rate: str
    avg_frame_rate: str
    time_base: Optional[str]
    start_pts: Optional[int]
    start_time: str
    duration_ts: float
    duration: float
    bit_rate: str
    bits_per_raw_sample: str
    nb_frames: int


class AudioStreamMeta(BaseModel):
    # 音频流元信息
    index: int
    codec_name: str
    codec_long_name: str
    profile: Optional[str]
    codec_type: str
    codec_tag_string: str
    codec_tag: str
    sample_fmt: str
    sample_rate: str
    channels: int
    channels_layout: Optional[str]
    bits_per_sample: int
    id: Optional[str]
    r_frame_rate: str
    avg_frame_rate: str
    time_base: str
    start_pts: Optional[int]
    start_time: Optional[float]
    duration_ts: float
    duration: float
    bit_rate: float
    nb_frame: Optional[int]


class FormatMeta(BaseModel):
    # 格式元信息
    filename: str
    nb_stream: Optional[int]
    nb_programs: Optional[int]
    format_name: str
    format_long_name: str
    start_time: Optional[float]
    duration: float
    size: int
    bit_rate: float
    probe_score: float


class Meta(BaseModel):
    # 总的元信息
    format_meta: Optional[FormatMeta]
    audio_stream: Optional[AudioStreamMeta]
    video_stream: Optional[VideoStreamMeta]

    def sample_rate(self):
        return eval(self.audio_stream.sample_rate)

    def frame_rate(self):
        return eval(self.video_stream.r_frame_rate)


def meta_from_json(info: Dict) -> Meta:
    codec_type2stream = {}
    format_meta = FormatMeta(**info['format'])
    for stream in info['streams']:
        codec_type2stream[stream['codec_type']] = stream
    audio_stream_json = codec_type2stream.get('audio')
    video_stream_json = codec_type2stream.get('video')
    meta = Meta(format_meta=format_meta)
    if audio_stream_json:
        meta.audio_stream = AudioStreamMeta(**audio_stream_json)
    if video_stream_json:
        meta.video_stream = VideoStreamMeta(**video_stream_json)
    return meta


def probe(file: str, show_log=False):
    # probe返回原始JSON串
    options = ["-print_format", "json", "-show_streams", "-show_format", ]
    _ffmpeg_common(options, show_log)
    a = ['ffprobe'] + options + [file]
    a = [str(i) for i in a]
    logger.info(f"{' '.join(a)}")
    resp = sp.check_output(a)
    return json.loads(str(resp, encoding='utf8'))


def get_meta(file: str, show_log=False):
    # get meta返回结构体
    return meta_from_json(probe(file, show_log))


def auto_detect_by_filename(file: str):
    _, ext = os.path.splitext(os.path.basename(file))
    want = None
    if ext in ('.mov', '.mp4'):
        want = 'video'
    elif ext in ('.mp3', '.wav'):
        want = 'audio'
    return want


audio_fmt2dtype = {
    's16le': "<i2",
    's16be': ">i2",
    "f32le": "<f4",
    "f32be": ">f4",
}
audio_dtype2fmt = {
    np.int16: "s16le",
    np.float32: 'f32le',
    np.float: 'f32le',
    np.float64: 'f64le',
    np.dtype("float64"): 'f64le',
    np.dtype("int16"): 's16le',
    np.dtype("float32"): "f32le",
}


class MediaType:
    video = 'video'
    audio = 'audio'


class ArrayReader:
    def __init__(self, cin, dtype, frame_shape):
        self.dtype = dtype
        self.frame_shape = frame_shape
        self.cin = cin

    def read(self, n: int = 0) -> np.ndarray:
        if n == 0:
            content = self.cin.read()
            self.cin.close()
        else:
            byte_count = np.prod(self.frame_shape) * n
            content = self.cin.read(byte_count)
        ans = np.frombuffer(content, self.dtype)
        ans = ans.reshape(-1, *self.frame_shape)
        return ans


class MediaFile:
    def __init__(self, meta: Meta, reader: ArrayReader):
        self.meta = meta
        self.reader = reader


def open_media(file: str, media_type: str = 'auto', out_audio_fmt="s16e", out_pix_fmt="rgb24", show_log=False) -> MediaFile:
    if media_type == 'auto' or not media_type:
        media_type = auto_detect_by_filename(file)
    if not os.path.exists(file):
        raise Exception(f'file not found {file}')
    if media_type not in ('video', 'audio'):
        raise Exception(f"cannot decide want video or audio by file {file} want={media_type}")
    meta = get_meta(file, show_log)
    if media_type == 'video' and not meta.video_stream or media_type == 'audio' and not meta.audio_stream:
        raise Exception(f"{file} don't have {media_type}")
    global_options = []
    _ffmpeg_common(global_options, show_log)
    output_options = []
    if media_type == 'video':
        output_options.extend([
            '-f', 'image2pipe',
            '-pix_fmt', out_pix_fmt,
            '-vcodec', 'rawvideo',
        ])
        a = ['ffmpeg'] + global_options + ['-i', file, ] + output_options + ['-']
        dtype = np.uint8
        width, height = meta.video_stream.width, meta.video_stream.height
        frame_shape = (height, width, 3)
    else:
        output_options.extend([
            '-f', out_audio_fmt,
            # "-sample_fmt", "s16",  # dont need
            # '-acodec', "pcm_s16le",
        ])
        channel = meta.audio_stream.channels
        a = ['ffmpeg'] + global_options + ['-i', file, ] + output_options + ['-']
        dtype = audio_fmt2dtype[out_audio_fmt]
        frame_shape = (channel,)
    logger.info(f"{' '.join(a)} dtype={dtype} shape={frame_shape}")
    p = sp.Popen(a, stdout=sp.PIPE)
    reader = ArrayReader(p.stdout, dtype, frame_shape)
    return MediaFile(meta, reader)


def read(file: str, media_type: str = 'auto', out_audio_fmt="s16le", out_pix_fmt='rgb24', show_log=False, ) -> (Meta, ArrayReader,):
    """
    :param file:
    :param show_log:
    :param media_type:'auto' 自动，'video' 视频，'audio' 音频
    :param show_log:
    :param audio_fmt:想要的音频数据类型
    :param pix_fmt:想要的视频的颜色类型
    :return:
    """
    info = open_media(file, media_type, out_audio_fmt=out_audio_fmt, out_pix_fmt=out_pix_fmt, show_log=show_log)
    return info.meta, info.reader.read()


class ArrayPipe:
    def __init__(self, dtype: np.dtype, frame_shape: Union[List[int], Tuple[int]], cin: IO, cout: IO):
        self.dtype = dtype
        self.frame_shape = frame_shape
        self.cin = cin
        self.cout = cout

    def write(self, a: np.ndarray):
        if a.dtype != self.dtype:
            raise Exception(f"error data type : expecting={self.dtype} current={a.dtype}")
        if a.shape[1:] != self.frame_shape:
            raise Exception(f"error data shape : expecting={self.frame_shape} current={a.shape}")
        self.cin.write(a.tobytes())


def get_writer(file: str, dtype, frame_shape, out_fmt: str, rate: int, media_type: str = None, show_log=False, ) -> ArrayPipe:
    """
    如果是写音频，meta必须包含sample_rate
    如果是写视频，meta必须包含r_frame_rate
    :param file:
    :param dtype:
    :param frame_shape:
    :param out_fmt:
    :param rate:
    :param show_log:
    :param media_type
    :return:
    """
    # 只能写一个视频或者写一个音频
    global_options = ['-y']  # 默认强制覆盖
    _ffmpeg_common(global_options, show_log)
    if media_type not in ('video', 'audio'):
        raise Exception(f"error file type {media_type}")
    if media_type == 'audio':
        if frame_shape in (1, 2):
            channels = frame_shape
        elif type(frame_shape) in (tuple, list) and len(frame_shape) == 1:
            channels = frame_shape[0]
        else:
            raise Exception(f"error shape {frame_shape}")
        # 根据data的数据类型确定-f参数的内容
        audio_fmt = audio_dtype2fmt[dtype]
        input_list = [
            "-f", audio_fmt,
            # 实验证明下面这两行其实是不需要的，只需要指定format即可。
            # "-sample_fmt", "s16",
            # '-acodec', "pcm_s16le",
            "-ar", rate,
            "-ac", channels,
            "-i", "-"
        ]
        out_options = ['-f', out_fmt, ]
        if out_fmt in ('mp4',) and file in ('-', 'pipe:1'):
            out_options.extend(['-movflags', 'frag_keyframe+empty_moov'])
    else:
        if not dtype == np.uint8:
            raise Exception(f"dataType must be uin8")
        if len(frame_shape) != 3 or frame_shape[-1] != 3:
            raise Exception(f"error shape {frame_shape}")
        height, width = frame_shape[:2]
        # 根据data的dtype和深度确定pix_fmt
        input_list = [
            "-r", rate,
            '-f', 'rawvideo',
            '-pix_fmt', 'rgb24',
            "-s", f"{width}x{height}",
            "-i", "-"
        ]
        out_options = ['-f', out_fmt, ]
    a = ['ffmpeg'] + global_options + input_list + out_options + [file]
    a = [str(i) for i in a]
    logger.info(f"{' '.join(a)}")
    p = sp.Popen(a, stdin=sp.PIPE, stdout=sp.PIPE)
    return ArrayPipe(dtype, frame_shape, p.stdin, p.stdout)


def thread_run(func_list, block=True):
    a = [threading.Thread(target=i) for i in func_list]
    for i in a:
        i.start()
    if block:
        for i in a:
            i.join()


def write(file: str, data: np.ndarray, rate: int, show_log=False, media_type: str = None):
    if not media_type:
        media_type = auto_detect_by_filename(file)
    if file not in ('', '-'):
        name, out_fmt = os.path.splitext(os.path.basename(file))
        out_fmt = out_fmt.lower()[1:]
    else:
        if media_type == 'video':
            out_fmt = 'mp4'
        else:
            out_fmt = 'mp3'
    p = get_writer(file, data.dtype, data.shape[1:], out_fmt, rate, media_type, show_log, )

    def write_thread():
        block_size = 1000
        i = 0
        while i < len(data):
            p.write(data[i:i + block_size])
            i += block_size
        p.cin.close()

    def read_thread():
        with open(file, 'wb') as cout:
            cout.write(p.cout.read())

    thread_run([write_thread, read_thread])


def play(file: str = '', writer: ArrayPipe = None, width: float = 0, height: float = 0,
         full_screen: bool = False,
         disable_autio=False,
         disable_video=False,
         disable_subtitles=False,
         disable_graphics=False,
         border_less=False,
         always_on_top=False,
         left: float = 0,
         top: float = 0,
         loop: int = -1,  # 0表示永远循环
         pos_by_seconds: float = 0,
         duration_by_seconds: float = 0,
         pos_by_bytes: int = 0,
         seek_interval_by_seconds: float = 10,
         show_mode: int = 0,  # 1 waves;2 rdft:离散傅里叶变化
         title: str = "",
         volume: float = -1,  # 音量
         show_log=False,  # 是否显示日志
         auto_exit=True,  # 播放完之后自动退出
         ):
    if not file and writer is None:
        raise Exception(f"file and writer cannot be both empty")
    options = []
    _ffmpeg_common(options, show_log)
    if full_screen:
        options.extend(["-fs"])
    if width:
        options.extend(['-x', round(width)])
    if height:
        options.extend(['-y', round(height)])
    if disable_autio:
        options.extend(['-an'])
    if disable_video:
        options.extend(['-vn'])
    if disable_subtitles:
        options.append("-sn")
    if disable_graphics:
        options.append("-nodisp")
    if always_on_top:
        options.append("-alwaysontop")
    if border_less:
        options.append("-noborder")
    if loop != -1:
        options.extend(['-loop', loop])
    if title:
        options.extend(['-window_title', title])
    if left:
        options.extend(['-left', left])
    if top:
        options.extend(['-top', top])
    if volume != -1:
        options.extend(['-volume', volume])
    if duration_by_seconds:
        options.extend(['-t', duration_by_seconds])
    if pos_by_bytes:
        options.extend(['-b', pos_by_bytes])
    if seek_interval_by_seconds and seek_interval_by_seconds != 10:
        options.extend(['-seek_interval', str(seek_interval_by_seconds)])
    if pos_by_seconds:
        options.extend(['-ss', pos_by_seconds])
    if show_mode:
        options.extend(['-showmode', show_mode])
    if auto_exit:
        options.extend(['-autoexit'])
    if writer is not None:
        file = '-'
    a = ["ffplay"] + options + [file]
    a = [str(i) for i in a]
    logger.info(f"{' '.join(a)}")
    play_pipe = sp.Popen(a, stdin=sp.PIPE, )
    if file != '-':
        play_pipe.wait()
        return
    if file == '-' and writer is not None:
        def read_and_write():
            block_size = 4096
            while 1:
                try:
                    content = writer.cout.read(block_size)
                    if len(content) == 0 and writer.cin.closed:
                        writer.cout.close()
                        break
                    play_pipe.stdin.write(content)
                except Exception as ex:
                    print(ex)
                    break
            play_pipe.stdin.close()

        def wait():
            play_pipe.wait()

        thread_run([read_and_write, wait], block=False)


def combine(file: str, video_file: str, audio_file: str, show_log=False, audio_loop=0, video_loop=0):
    # 将视频和音频融合在一起
    if video_file is None and audio_file is None:
        raise Exception("video and audio are both empty")
    input_list = []
    if video_file:
        if video_loop:
            input_list.extend(['-stream_loop', video_loop])
        input_list.extend(["-i", video_file])
    if audio_file:
        if audio_loop:
            input_list.extend(['-stream_loop', audio_loop])
        input_list.extend(["-i", audio_file])
    global_options = ['-y']  # 默认强制覆盖
    _ffmpeg_common(global_options, show_log)
    options = ["-map", "1:a", "-map", "0:v"]
    a = ['ffmpeg'] + global_options + input_list + options + [file]
    a = [str(i) for i in a]
    logger.info(f"{' '.join(a)}")
    sp.check_call(a)


def print_record_devices():
    if platform.system() == "Darwin":
        a = ['ffmpeg',
             '-f', 'avfoundation',
             '-list_devices', 'true',
             '-i', ""]
        a = [str(i) for i in a]
        logger.info(f"{' '.join(a)}")
        res = sp.check_output(a)
        print(str(res, encoding='utf8'))
    else:
        raise NotImplementedError


def get_record_pipe(video_src, audio_src, output_file: str, show_log=False) -> sp.Popen:
    if platform.system() == "Darwin":
        options = []
        _ffmpeg_common(options, show_log)
        a = ['ffmpeg', ] + options + ['-y', '-f', 'avfoundation', '-i', f"{video_src}:{audio_src}", output_file]
        a = [str(i) for i in a]
        logger.info(f"{' '.join(a)}")
        p = sp.Popen(a, stdout=sp.PIPE)
        return p
    else:
        raise NotImplementedError
