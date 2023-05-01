from skvideo.datasets import bigbuckbunny

import mediapy as mp


def test_audio():
    """
    读取mp4的音频并保存
    """
    meta, data = mp.read("../imgs/taylor.mp4", media_type='audio')
    print(data.shape, data.dtype)
    # 把音频文件单独写出去，然后播放
    mp.write("taylor.mp3", data, meta.audio_stream.sample_rate, show_log=False)
    print(mp.get_meta('taylor.mp3'))


def test_video():
    filepath = bigbuckbunny()
    meta, a = mp.read(filepath)
    mp.write('a.mp4', a, meta.frame_rate())
    """
    ffmpeg -y -f rawvideo -pix_fmt rgb24 -s 680x480 -i - outputvideo.mp4
    """
