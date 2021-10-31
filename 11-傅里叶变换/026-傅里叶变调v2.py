import numpy as np

import mediapy as mp

# 生日快乐歌
birthday = """
5 5 6 5 1^ 7
5 5 6 5 2^ 1^
5 5 5^ 3^ 1^ 7 6
4^ 4^ 3^ 1^ 2^ 1^ 1^
"""
rate, a = mp.nmn.get_float_array(birthday, rate=10000)
b = np.fft.fft(a)
bei = 2
c = np.zeros(len(b), dtype=np.complex)
ind_map = np.arange(len(b))
ind_map[:len(b) // 2] *= 2
ind_map[len(b) // 2:] = 0  # 把高位部分支撑0
c[ind_map] = b
d = np.fft.ifft(c)
print(a.shape, b.shape, c.shape, d.shape, )
print(a.dtype, b.dtype, c.dtype, d.dtype)
e = np.real(d)
# e = np.vstack([e[:len(e) // 2], e[len(e) // 2:]]).reshape(-1)
print(e.shape, e.dtype)
mp.write("a.wav", e, rate=rate)
mp.play("a.wav")
mp.write("b.wav", a, rate=rate)
mp.play("b.wav")
meta_a = mp.get_meta("a.wav")
meta_b = mp.get_meta("b.wav")
print(meta_a.audio_stream.duration, meta_b.audio_stream.duration)
print(meta_a.audio_stream.sample_rate, meta_b.audio_stream.sample_rate)
