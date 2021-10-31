"""
让每一段拼接的时候时长都正好跑完一个周期，这样每一段开始的相位都是0
"""
import numpy as np
import pylab as plt

import mediapy as mp

s = "1 7 1 7 1 7 1 7 1 7 1 7"
rate = 8000
book = mp.nmn.content2book(s, 0.3)
a = []
for freq, duration in book:
    if freq == 0:
        continue
    cycle_count = round(duration * freq)  # 周期个数
    duration = cycle_count / freq
    a.append(mp.nmn.freq2wave(freq, rate, duration, freq_wav_type=mp.nmn.FreqWaveType.constant))
sz = np.cumsum([len(i) for i in a])
print('各个长度', sz)
a = np.concatenate(a)
print(len(a))
print(a.dtype)
mid = sz[2]
x = np.arange(len(a))
plt.plot(x[mid - 30:mid + 30], a[mid - 30:mid + 30])
plt.vlines(x[mid], np.min(a), np.max(a))
plt.show()
mp.write('a.wav', a, rate)
mp.play("a.wav")
