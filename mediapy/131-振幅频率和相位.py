"""
傅里叶变换的实质就是把波形拆成若干个正弦波

一个正弦波有：振幅，频率，相位三个属性。
对应到声音上就是：响度，音调，音色。
多个正弦波相位组合决定了音色，因此音色才具有如此丰富多彩的组合。

"""
import numpy as np

import mediapy as mp

rate = 4000
rate, a = mp.nmn.get_float_array("1 2 3 4 5 6 7 6 5 4 3 2 1", rate=rate)
b = np.fft.fft(a)
A = np.abs(b)  # 能量
angle = np.angle(b)  # 相位
freq = np.arange(len(b)) / len(a) * rate
import pylab as plt

plt.plot(freq, A)
plt.xlim(0, 800)
plt.show()
duration = len(a) / rate
c = 0
"""
A表示振幅，angle表示相位，则
f(t)=sum Acos(w*x-angle)
亦等于 sum A sin(w*x+(np.pi/2-(-angle)))
"""
for f, e, phi in zip(freq, A, angle):
    c = c + mp.nmn.freq2wave(f, rate, duration, np.pi / 2 + phi, e, freq_wav_type=mp.nmn.FreqWaveType.constant)
c /= len(a)
print(a.shape, a.dtype)
print(c.shape, c.dtype)
print(c[:10])
print(a[:10])
d = np.fft.ifft(b)
print(d[:10])
fig, axes = plt.subplots(3, 1)
one, two, three = axes.reshape(-1)
one.plot(a[:100])
two.plot(c[:100])
three.plot(d[:100])
print(np.allclose(d, a))
plt.show()
mp.write('a.wav', c, rate)
# mp.play('a.wav')
