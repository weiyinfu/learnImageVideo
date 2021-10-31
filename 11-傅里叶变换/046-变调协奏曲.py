import numpy as np
from tqdm import tqdm

import mediapy as mp

# 生日快乐歌
birthday = """
5 5 6 5 1^ 7
5 5 6 5 2^ 1^
5 5 5^ 3^ 1^ 7 6
4^ 4^ 3^ 1^ 2^ 1^ 1^
"""
rate, a = mp.nmn.get_float_array(birthday, rate=10000)


def sfft(a, rate: int, window: int, freq_bei: float, duration_bei: float, top: int = 4):
    b = []
    phi = 0
    for i in tqdm(range(0, len(a), window)):
        f = np.fft.fft(a[i:i + window])
        enegy = np.abs(f)
        ind = np.argmax(enegy[:len(f) // 2])
        freq = ind / len(f) * rate
        freq = freq * freq_bei
        duration = window / rate * duration_bei
        part = mp.nmn.freq2wave(freq, rate, duration=duration, phi=phi, freq_wav_type=mp.nmn.FreqWaveType.constant)
        b.append(part)
        # 对于短时傅里叶变换，维持原相位效果最好
        phi += freq * np.pi * 2 * duration
    return mp.nmn.concatenate_clips(b)


high = sfft(a, rate=rate, window=500, freq_bei=2, duration_bei=1, top=1)
low = sfft(a, rate=rate, window=500, freq_bei=0.5, duration_bei=1, top=1)
for i in (high, low, a):
    print(i.shape, i.dtype)
sz = max(len(high), len(low), len(a))
b = np.zeros(sz)
weight = [0.5, 1, 0.5]
b[:len(high)] += high * weight[0]
b[:len(low)] += low * weight[-1]
b[:len(a)] += a * weight[1]
b /= np.sum(weight)
mp.write("a.wav", b, rate=rate)
# mp.play("a.wav")
meta, c = mp.read("a.wav")
# 变调协奏曲再变调，将会失败，因为以上sfft只能检测出强度最大的音调并变调
d = sfft(c, rate=rate, window=300, freq_bei=1, duration_bei=1)
mp.write('b.wav', d, rate)
mp.play('b.wav')
