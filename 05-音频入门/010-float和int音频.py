import numpy as np
import pylab as plt

import mediapy as mp

"""
音频有float和int两种表示形式，int都是带符号的。
float*max positive int=int
例如float32格式的音频都是0到1之间的数值，乘以32768（2**15）便得到s16格式的音频
"""
_, d1 = mp.read("../imgs/taylor.wav")
_, d2 = mp.read("../imgs/taylor.wav", out_audio_fmt="f32be")
d1 = d1[:, 1]
d2 = d2[:, 1]

ans = d1 / d2
print(np.min(d2), np.max(d2))
print(d1[:10], d2[:10], 2 ** 15 * d2[:10])
print(ans[:10])
plt.plot(ans)
plt.show()
