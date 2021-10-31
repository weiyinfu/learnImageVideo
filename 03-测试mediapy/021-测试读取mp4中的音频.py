import mediapy as mp

"""
读取视频中的音频
"""
meta, data = mp.read("../imgs/taylor.mp4", media_type='audio')
print(data.shape, data.dtype)
# 把音频文件单独写出去，然后播放
mp.write("taylor.mp3", data, meta.sample_rate(), show_log=False)

print("=========")
xmeta, x = mp.read("./taylor.mp3")
ymeta, y = mp.read("../imgs/taylor.mp3")
print(x.shape, y.shape, x.dtype, y.dtype)
print(xmeta)
print(ymeta)
