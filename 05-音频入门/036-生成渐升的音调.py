"""
根据频率产生声音
"""
import numpy as np

import mediapy as mp

max_freq = 2000
ma = [261.626, 293.665, 329.628, 349.228, 391.995, 440.000, 493.883, ]


def get(freq, rate, duration):
    sz = int(duration * rate)
    a = np.arange(sz)
    t = a / len(a) * duration
    return np.sin(np.pi * 2 * freq * t)


rate = max_freq * 2
a = np.concatenate([get(ma[i], rate, 1) for i in range(len(ma))])
a = (a * (2 ** 13)).astype(np.int16)
print("文件长度", len(a), a.dtype)
mp.write("a.wav", a, rate=rate)
mp.play("./a.wav")
