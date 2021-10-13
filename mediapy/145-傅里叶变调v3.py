import numpy as np
from tqdm import tqdm

import mediapy as mp

"""
变调无法直接使用傅里叶逆变换
长时间傅里叶变换复杂度为n^2，所以平时常用的都是短时间傅里叶变换分段处理再拼接
"""
# 生日快乐歌
birthday = """
5 5 6 5 1^ 7
5 5 6 5 2^ 1^
5 5 5^ 3^ 1^ 7 6
4^ 4^ 3^ 1^ 2^ 1^ 1^
"""
birthday = """ 
5 5 5^ 3^ 1^ 7 6
4^ 4^ 3^ 1^ 2^ 1^ 1^
"""
rate, a = mp.nmn.get_float_array(birthday, rate=2000)
b = np.fft.fft(a)
bei = 2.1
freq = np.arange(len(a)) / len(a) * rate
# freq[len(b) // 2 + 1:] -= freq[-1]
A = np.abs(b)
angle = np.angle(b)
duration = len(a) / rate
c = 0
for f, e, phi in zip(tqdm(freq), A, angle):
    c = c + mp.nmn.freq2wave(f * bei, rate, duration, np.pi / 2 + phi, e, freq_wav_type=mp.nmn.FreqWaveType.constant)
c /= len(b)
print(a.shape, b.shape, c.shape)
print(a.dtype, b.dtype, c.dtype)


def play():
    mp.write("a.wav", c, rate=rate)
    mp.play("a.wav")
    mp.write("b.wav", a, rate=rate)
    mp.play("b.wav")
    meta_a = mp.get_meta("a.wav")
    meta_b = mp.get_meta("b.wav")
    print(meta_a.audio_stream.duration, meta_b.audio_stream.duration)
    print(meta_a.audio_stream.sample_rate, meta_b.audio_stream.sample_rate)


play()
