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


e = sfft(a, rate=rate, window=500, freq_bei=1.8, duration_bei=2, top=1)
# e = mp.ap.sfft(a, rate=rate, window=500, freq_bei=2.1, duration_bei=2.1, top=1)
mp.write("a.wav", e, rate=rate)
mp.play("a.wav")
mp.write("b.wav", a, rate=rate)
mp.play("b.wav")
meta_a = mp.get_meta("a.wav")
meta_b = mp.get_meta("b.wav")
print(meta_a.audio_stream.duration, meta_b.audio_stream.duration)
print(meta_a.audio_stream.sample_rate, meta_b.audio_stream.sample_rate)
