import mediapy as mp

"""
读取视频中的音频
"""
meta, data = mp.read("../imgs/taylor.mp4", filetype='audio')
print(data.shape, data.dtype)
# 把音频文件单独写出去，然后播放
mp.write("taylor.mp3", data, meta.audio_stream.get_sample_rate(), show_log=False)
