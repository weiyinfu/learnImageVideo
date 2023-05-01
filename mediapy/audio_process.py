import numpy as np
from tqdm import tqdm

import mediapy.number_music_notation as nmn
"""
音频处理
"""

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
        part = nmn.freq2wave(freq, rate, duration=duration, phi=phi, freq_wav_type=nmn.FreqWaveType.constant)
        b.append(part)
        # 对于短时傅里叶变换，维持原相位效果最好
        phi += freq * np.pi * 2 * duration
    return nmn.concatenate_clips(b)
