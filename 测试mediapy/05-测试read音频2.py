import matplotlib.pyplot as plt
import numpy as np
import scipy.io.wavfile as wav

import mediapy as mp

"""
一个读mp3，一个读wav，验证结果正确性

结果是不一样的，但是大致上比较相似。不太理解误差从何处来。
"""
meta, data = mp.read("../imgs/taylor.mp3")
rate, data2 = wav.read("../imgs/taylor.wav")
print(f"rate={rate}")
print(data.shape, data2.shape)
print(data.dtype, data2.dtype)
print(np.all(data == data2))
print(data[:5], data2[:5])
print(rate, meta.audio_stream.sample_rate)
x, y = data[:, 1], data2[:, 1]
plt.plot(x[:1000])
plt.plot(y[:1000])
plt.show()
