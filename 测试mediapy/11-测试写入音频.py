import mediapy as mp

"""
读取mp4的音频并保存
"""
meta, data = mp.read("../imgs/taylor.mp4", media_type='audio')
print(data.shape, data.dtype)
# 把音频文件单独写出去，然后播放
mp.write("taylor.mp3", data, meta.audio_stream.sample_rate, show_log=False)
print(mp.get_meta('taylor.mp3'))
