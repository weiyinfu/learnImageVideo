import pylab as plt
import numpy as np
import mediapy as mp

"""
B样条平滑虽然能够让波形平滑，但是依旧无法让声音听起来柔顺。  
声音听起来柔和的关键因素就是相位。  
"""
s = "1 7 1 7 1 7 1 7 1 7 1 7"
rate = 8000
book = mp.nmn.content2book(s, 0.3)
a = []
for freq, duration in book:
    a.append(mp.nmn.freq2wave(freq, rate, duration, freq_wav_type=mp.nmn.FreqWaveType.constant))
b = mp.nmn.concatenate_clips(a)
sz = np.cumsum([len(i) for i in a])


def show(mid):
    print(mid)
    plt.plot(b[mid - 30:mid + 30])
    # 第二种方法
    phi = 0
    c = []
    for freq, duration in book:
        c.append(mp.nmn.freq2wave(freq, rate, duration, phi=phi, freq_wav_type=mp.nmn.FreqWaveType.constant))
        phi += freq * np.pi * 2 * duration
    c = np.concatenate(c)
    plt.plot(c[mid - 30:mid + 30])
    plt.show()


print(sz)
show(sz[5])
