import json
import os.path
import platform
import subprocess as sp
import threading
from typing import Optional, Dict, List, Tuple, IO, Union, Callable

import numpy as np
from pydantic import BaseModel

from mediapy.log import logger

"""
参考ffmpeg文档，使用python包装ffmpeg，用于生成视频、音频，执行ffmpeg的命令
https://www.ffmpeg.org/documentation.html
"""


def _ffmpeg_common(options: List[str], show_log: bool):
    """
    用于生成命令的公共参数。公共参数的作用包括：隐藏掉ffmpeg的banner，设置日志级别等
    :param options: 已有的options列表，是一个字符串数组
    :param show_log: 是否显示日志，如果传False，则日志级别为error级别，日志量会比较少
    :return:
    """
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
    sample_aspect_ratio: Optional[str]
    display_aspect_ratio: Optional[str]
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
    duration_ts: Optional[float]
    duration: Optional[float]
    bit_rate: Optional[str]
    bits_per_raw_sample: str
    nb_frames: Optional[int]


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
    duration_ts: Optional[float]
    duration: Optional[float]
    bit_rate: Optional[float]
    nb_frame: Optional[int]


class FormatMeta(BaseModel):
    # 格式元信息
    filename: str
    nb_stream: Optional[int]
    nb_programs: Optional[int]
    format_name: str
    format_long_name: str
    start_time: Optional[float]
    duration: Optional[float]
    size: int
    bit_rate: Optional[float]
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

    def format_name(self):
        return self.format_meta.format_name


def meta_from_json(info: Dict) -> Meta:
    """
    把一个Dict类型的meta信息转成Python中的Meta数据结构
    :param info: Dict类型的meta信息，可以与JSON等价
    :return: Meta结构体
    """
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


def probe(file: str, show_log=False) -> Dict:
    """
    封装ffmpeg的probe命令，探测给定文件的信息，返回一个JSON Dict
    :param file: 需要探测的文件名称
    :param show_log: 是否显示日志，默认为False
    :return: 一个Dict，key表示meta信息的名称，value表示meta信息的取值
    """
    options = ["-print_format", "json", "-show_streams", "-show_format", ]
    _ffmpeg_common(options, show_log)
    a = ['ffprobe'] + options + [file]
    a = [str(i) for i in a]
    logger.info(f"{' '.join(a)}")
    resp = sp.check_output(a)
    return json.loads(str(resp, encoding='utf8'))


def get_meta(file: str, show_log=False) -> Meta:
    """
    类似probe函数，唯一的区别在于get_meta返回一个Python结构体，而probe直接返回原始数据
    :param file: 需要探测的文件名称，例如可以是mp4或者mp3
    :param show_log: 是否显示日志，默认为False
    :return:
    """
    # get meta返回结构体
    return meta_from_json(probe(file, show_log))


class MediaType:
    # 媒体的类型，包括视频和音频两种格式
    video = 'video'
    audio = 'audio'


def detect_media_type(file: str) -> str:
    """
    根据后缀名探测文件的媒体类型
    :param file: 给定的文件名称
    :return: 返回MediaType
    """
    media_type = None
    ext = get_fmt_by_filename(file)
    if ext in ('mov', 'mp4', 'matroska'):
        media_type = MediaType.video
    elif ext in ('mp3', 'wav'):
        media_type = MediaType.audio
    return media_type


class AudioFormat:
    # 音频的波形数据存储格式，主要使用大头小头字节序，使用的位数，使用整型还是浮点型三种情况组合。
    s16le = 's16le'  # 有符号 16位 整型，小头序
    s16be = 's16be'  # 有符号 16位 整型，大头序
    s32le = 's32le'  # 有符号 32位 整型，小头序
    s32be = 's32be'  # 有符号 32位 整型，大头序
    s64le = 's64le'  # 有符号 64位 整型，小头序
    s64be = 's64be'  # 有符号 64位 整型，大头序
    f32le = 'f32le'  # 浮点数32位，小头序
    f32be = 'f32be'  # 浮点数32位，大头序
    f64le = 'f64le'  # 浮点数64位，小头序
    f64be = 'f64be'  # 浮点数64位，大头序


# 音频格式与numpy中dtype类型描述的映射
audio_fmt2dtype = {
    's16le': "<i2",
    's16be': ">i2",
    's32le': '<i4',
    's32be': '>i4',
    's64le': '<i8',
    's64be': '>i8',
    "f32le": "<f4",
    "f32be": ">f4",
    'f64le': '<f8',
    'f64be': '>f8',
}
# numpy类型与音频类型的映射
audio_dtype2fmt = {
    np.int16: AudioFormat.s16le,
    np.int32: AudioFormat.s32le,
    np.int64: AudioFormat.s64le,
    np.float32: AudioFormat.f32le,
    np.float64: AudioFormat.f64le,
    np.dtype("int16"): AudioFormat.s16le,
    np.dtype("int32"): AudioFormat.s32le,
    np.dtype("int64"): AudioFormat.s64le,
    np.dtype("float32"): AudioFormat.f32le,
    np.dtype("float64"): AudioFormat.f64le,
}

# 一帧数据的形状，用于描述数据的尺寸。可以是一个int元组、一个int数值（表示一维数组），一个int列表
FrameShape = Union[List[int], Tuple, int]


class ArrayMeta:
    # 数组的meta信息，包含数组的数据类型和数组的尺寸信息
    def __init__(self, dtype, frame_shape: FrameShape):
        self.dtype = dtype
        self.frame_shape = frame_shape

    def __repr__(self):
        return f"dtype={self.dtype},frame_shape={self.frame_shape}"


def connect_stream(cin: IO, cout: IO, block=False) -> List[threading.Thread]:
    # 开启一个线程从cin里面读数据，然后把数据写入到cout中
    def connect():
        block_size = 40960
        try:
            while 1:
                content = cin.read(block_size)
                # logger.info(f"{len(content)}")
                if len(content) == 0:
                    cout.close()
                    break
                cout.write(content)
                cout.flush()
        except Exception as ex:
            logger.error(f"connect error {ex}")
        cin.close()
        cout.close()

    return thread_run([connect], block=block)


class ArrayPipe:
    # 一个管道就是一个命令的封装，cin为它的输入流，cout为它的输出流
    def __init__(self, cin: IO, cout: IO, input_meta: ArrayMeta = None, output_meta: ArrayMeta = None):
        self.input_meta = input_meta
        self.output_meta = output_meta
        self.cin = cin
        self.cout = cout
        self.threads = []

    def write(self, a: np.ndarray):
        if self.cin.closed:
            logger.info(f"cin closed already")
            return
        if a.dtype != self.input_meta.dtype:
            raise Exception(f"error data type : expecting={self.input_meta.dtype} current={a.dtype}")
        if len(a.shape) == 1 and self.input_meta.frame_shape == 1:
            pass
        elif list(a.shape[1:]) != list(self.input_meta.frame_shape):
            raise Exception(f"error data shape : expecting={self.input_meta.frame_shape} current={a.shape}")
        content = a.tobytes()
        if len(content) == 0:
            return
        self.cin.write(content)
        self.cin.flush()

    def read(self, n: int = 0) -> Union[np.ndarray, None]:
        if self.cout.closed:
            return
        if n == 0:
            content = self.cout.read()
            self.cout.close()
        else:
            byte_count = np.prod(self.output_meta.frame_shape) * n * np.dtype(self.output_meta.dtype).itemsize
            content = self.cout.read(byte_count)
            if len(content) != byte_count:
                logger.warn(f"reader not complete:expect={byte_count},real got={len(content)}")
                return None
        if len(content) == 0:
            return
        ans = np.frombuffer(content, self.output_meta.dtype)
        ans = ans.reshape(-1, *self.output_meta.frame_shape)
        return ans

    def add_cin(self, cin: IO, block=False):
        self.threads.extend(connect_stream(cin, self.cin, block))
        self.cin = cin

    def add_cout(self, cout: IO, block=False):
        self.threads.extend(connect_stream(self.cout, cout, block))
        self.cout = cout

    def join(self):
        for i in self.threads:
            i.join()


def connect_pipe(pre: ArrayPipe, nex: ArrayPipe) -> ArrayPipe:
    ans = ArrayPipe(pre.cin, nex.cout, pre.input_meta, nex.output_meta)
    threads = connect_stream(pre.cout, nex.cin)
    threads = pre.threads + threads + nex.threads
    ans.threads = threads
    return ans


def get_reader(file: str, media_type: str, frame_shape: FrameShape, out_audio_fmt='s16e', out_pix_fmt='rgb24', out_video_fmt='image2pipe', show_log=False) -> ArrayPipe:
    """
    说明：file参数是必需的，有些文件格式必须是seekable的，这就要求数据流不能从stdin里面读入，所以必须传递file参数。当不需要的时候，传递-然后处理stdin即可。
    :param file:
    :param media_type:
    :param frame_shape:
    :param out_audio_fmt:
    :param out_pix_fmt:
    :param out_video_fmt:
    :param show_log:
    :return:
    """
    global_options = []
    _ffmpeg_common(global_options, show_log)
    output_options = []
    if media_type == 'video':
        output_options.extend([
            '-f', out_video_fmt,
            '-pix_fmt', out_pix_fmt,
            '-vcodec', 'rawvideo',
        ])
        dtype = np.uint8
        input_options = []
        a = ['ffmpeg'] + global_options + input_options + ['-i', file, ] + output_options + ['-']
    else:
        output_options.extend([
            '-f', out_audio_fmt,
            # "-sample_fmt", "s16",  # dont need
            # '-acodec', "pcm_s16le",
        ])
        a = ['ffmpeg'] + global_options + ['-i', file, ] + output_options + ['-']
        dtype = audio_fmt2dtype[out_audio_fmt]
    a = [str(i) for i in a]
    logger.info(f"{' '.join(a)} dtype={dtype} shape={frame_shape}")
    p = sp.Popen(a, stdin=sp.PIPE, stdout=sp.PIPE)
    reader = ArrayPipe(cin=p.stdin, cout=p.stdout, output_meta=ArrayMeta(dtype, frame_shape, ))
    return reader


class MediaFile:
    # media_file提供迭代器类型的读入
    def __init__(self, meta: Meta, reader: ArrayPipe):
        self.meta = meta
        self.reader = reader


def open_media(file: str, media_type: str = '', out_audio_fmt="s16e", out_pix_fmt="rgb24", show_log=False) -> MediaFile:
    if media_type in ('auto', '', None):
        media_type = detect_media_type(file)
    if not os.path.exists(file):
        raise Exception(f'file not found {file}')
    if media_type not in ('video', 'audio'):
        raise Exception(f"cannot decide want video or audio by file {file} media_type={media_type}")
    meta = get_meta(file, show_log)
    if media_type == 'video' and not meta.video_stream or media_type == 'audio' and not meta.audio_stream:
        raise Exception(f"{file} don't have {media_type}")
    if media_type == MediaType.video:
        width, height = meta.video_stream.width, meta.video_stream.height
        frame_shape = (height, width, 3)
    else:
        channel = meta.audio_stream.channels
        frame_shape = (channel,)
    reader = get_reader(file, media_type, frame_shape, out_audio_fmt, out_pix_fmt, show_log=show_log)
    return MediaFile(meta, reader)


def read(file: str, media_type: str = 'auto', out_audio_fmt="s16le", out_pix_fmt='rgb24', show_log=False, ) -> (Meta, np.ndarray,):
    """
    :param file:
    :param show_log:
    :param media_type:'auto' 自动，'video' 视频，'audio' 音频
    :param show_log:
    :param out_audio_fmt:想要的音频数据类型
    :param out_pix_fmt:想要的视频的颜色类型
    :return:
    """
    info = open_media(file, media_type, out_audio_fmt=out_audio_fmt, out_pix_fmt=out_pix_fmt, show_log=show_log)
    return info.meta, info.reader.read()


def get_writer(file: str, dtype, frame_shape: FrameShape, out_fmt: str, rate: int, media_type, show_log=False, ) -> ArrayPipe:
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
    if media_type not in (MediaType.video, MediaType.audio):
        raise Exception(f"error file type {media_type}")
    if media_type == MediaType.audio:
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
        out_options = []
        if file in ('-', ''):
            out_options.extend(['-f', out_fmt, ])
    else:
        if not dtype == np.uint8:
            raise Exception(f"dataType must be uin8")
        if len(frame_shape) != 3 or frame_shape[-1] != 3:
            raise Exception(f"error shape {frame_shape}")
        height, width = frame_shape[:2]
        input_list = [
            "-r", rate,
            '-f', 'rawvideo',
            '-pix_fmt', "rgb24",
            # '-vcodec', 'rawvideo',
            # "-pixel_format", "rgb24",
            "-s", f"{width}x{height}",
            "-i", "-"
        ]
        out_options = [
            '-f', out_fmt,
            # '-pix_fmt', 'rgb24',
        ]
        if out_fmt in ('mp4',) and file in ('-', ''):
            out_options.extend(['-movflags', 'frag_keyframe+empty_moov'])

    a = ['ffmpeg'] + global_options + input_list + out_options + [file]
    a = [str(i) for i in a]
    logger.info(f"{' '.join(a)}")
    p = sp.Popen(a, stdin=sp.PIPE, stdout=sp.PIPE)
    return ArrayPipe(cin=p.stdin, cout=p.stdout, input_meta=ArrayMeta(dtype, frame_shape, ))


def thread_run(func_list: List[Callable], block=False) -> List[threading.Thread]:
    a = [threading.Thread(target=i, name=f'{i.__name__}') for i in func_list]
    for i in a:
        i.daemon = True
        i.start()
    if block:
        for i in a:
            i.join()
    return a


def get_fmt_by_filename(file: str) -> str:
    name, out_fmt = os.path.splitext(os.path.basename(file))
    out_fmt = out_fmt.lower()[1:]
    return out_fmt


def write(file: str, data: np.ndarray, rate: int, show_log=False, media_type: str = None, ):
    if not media_type:
        media_type = detect_media_type(file)
    if file not in ('', '-'):
        out_fmt = get_fmt_by_filename(file)
    else:
        if media_type == 'video':
            out_fmt = 'mp4'
        else:
            out_fmt = 'mp3'
    if len(data.shape) == 1:
        if media_type == MediaType.audio:
            shape = 1
        else:
            raise Exception(f"error video data.shape {data.shape}")
    else:
        shape = data.shape[1:]
    p = get_writer(file, data.dtype, shape, out_fmt, rate, media_type, show_log=show_log, )
    f = open(file, 'wb')
    p.add_cout(f, block=False)
    p.cin.write(data.tobytes())
    p.cin.close()
    p.join()


def play(file: str, width: float = 0, height: float = 0,
         full_screen: bool = False,
         disable_audio=False,
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
         ) -> ArrayPipe:
    options = []
    _ffmpeg_common(options, show_log)
    if full_screen:
        options.extend(["-fs"])
    if width:
        options.extend(['-x', round(width)])
    if height:
        options.extend(['-y', round(height)])
    if disable_audio:
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
    if not title and file not in ('', '-'):
        title = file
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
    options.extend(['-noinfbuf'])
    a = ["ffplay"] + options + [file]
    a = [str(i) for i in a]
    logger.info(f"{' '.join(a)}")
    p = sp.Popen(a, stdin=sp.PIPE, )
    pipe = ArrayPipe(cin=p.stdin, cout=p.stdout, input_meta=None, output_meta=None)
    return pipe


def play_pipe(pipe: ArrayPipe,
              width: float = 0, height: float = 0,
              full_screen: bool = False,
              disable_audio=False,
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
    if not title:
        title = '无题'
    p = play(file='-', width=width, height=height, full_screen=full_screen, disable_audio=disable_audio, disable_video=disable_video, disable_subtitles=disable_subtitles, disable_graphics=disable_graphics, border_less=border_less, always_on_top=always_on_top, left=left, top=top, loop=loop, pos_by_seconds=pos_by_seconds, duration_by_seconds=duration_by_seconds, pos_by_bytes=pos_by_bytes, seek_interval_by_seconds=seek_interval_by_seconds, show_mode=show_mode, title=title, volume=volume,
             show_log=show_log, auto_exit=auto_exit)
    p = connect_pipe(pipe, p, )
    return p


def combine(file: str, video_file: str, audio_file: str, show_log=False, audio_loop=0, video_loop=0, by_video_time=True):
    # 将视频和音频融合在一起
    if video_file is None and audio_file is None:
        raise Exception("video and audio are both empty")
    input_list = []
    if video_file:
        if video_loop:
            input_list.extend(['-stream_loop', video_loop])
        input_list.extend(["-i", video_file])
    video_duration = 0
    if video_file:
        video_meta = get_meta(video_file)
        video_duration = float(video_meta.video_stream.duration)
    if audio_file:
        if audio_loop:
            input_list.extend(['-stream_loop', audio_loop])
        if by_video_time and video_duration:
            input_list.extend(['-t', video_duration])
        input_list.extend(["-i", audio_file])
    global_options = ['-y']  # 默认强制覆盖
    _ffmpeg_common(global_options, show_log)
    options = ["-map", "1:a", "-map", "0:v"]
    a = ['ffmpeg'] + global_options + input_list + options + [file]
    a = [str(i) for i in a]
    logger.info(f"{' '.join(a)}")
    sp.check_call(a)


def print_record_devices(show_log=False):
    # 打印播放设备信息
    if platform.system() == "Darwin":

        options = []
        a = ['ffmpeg', ] + options + [
            '-f', 'avfoundation',
            '-list_devices', 'true',
            '-i', '-',
        ]
        a = [str(i) for i in a]

        logger.info(f"{' '.join(a)}")
        try:
            res = sp.check_call(a)
        except:
            pass
    else:
        raise NotImplementedError


def get_record_pipe(video_src: str, audio_src: str, rate: int = 20, audio_rate=16000, width=1280, height=720, duration=0., show_log=False) -> ArrayPipe:
    """
    获取录音机录制数据，仅在苹果系统上可用
    :param video_src:
    :param audio_src:
    :param rate:
    :param audio_rate:
    :param width:
    :param height:
    :param duration:
    :param show_log:
    :return:
    """
    if platform.system() == "Darwin":
        global_options = ['-y']
        _ffmpeg_common(global_options, show_log)
        input_options = [
            '-f', 'avfoundation',
            '-r', rate,
            # '-ar', audio_rate,
        ]
        if duration:
            input_options.extend(['-t', duration, ])
        output_options = [
            '-f', 'matroska',
            '-s', f'{width}x{height}',
        ]
        a = ['ffmpeg', ] + global_options + input_options + ['-i', f"{video_src}:{audio_src}", ] + output_options + ['-']
        a = [str(i) for i in a]
        logger.info(f"{' '.join(a)}")
        p = sp.Popen(a, stdout=sp.PIPE)
        return ArrayPipe(cin=p.stdin, cout=p.stdout, output_meta=ArrayMeta(np.uint8, [height, width, 3]))
    else:
        raise NotImplementedError


def record(video_src: str, audio_src: str, rate: int, media_type: str, frame_shape: FrameShape, show_log=False):
    p = get_record_pipe(video_src, audio_src, rate, show_log)
    reader = get_reader('-', media_type, frame_shape, show_log=show_log)
    reader = connect_pipe(p, reader)
    return reader


def record_file_by_time(video_src: str, audio_src: str, output_file: str, rate: int = 20, sample_rate=16000, width=1280, height=720, duration: float = 10., show_log=False):
    p = get_record_pipe(video_src, audio_src, rate, duration=duration, show_log=show_log)
    with open(output_file, 'wb') as f:
        p.add_cout(f, block=True)


def change_format(input_file: str, output_file: str, pix_fmt: str):
    """
    使用ffmpeg修改视频格式
    :param input_file: 输入文件名称
    :param output_file: 输出文件名称
    :param pix_fmt: 像素格式
    :return:
    """
    options = []
    _ffmpeg_common(options, False)
    a = ['ffmpeg'] + options + ['-y', '-i', input_file, '-pix_fmt', pix_fmt, output_file]
    sp.check_call(a)
