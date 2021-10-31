import numpy as np

import mediapy as mp

"""
相位拼接和加权拼接各有利弊：
相位拼接具有更好的数学特征，适合频域简单且已知的情况。  
加权拼接具有更好的通用性，适合拼接任意类型的波形。  

相位拼接的要点：y1=Asin(w1*x+phi1),y2=Bsin(w2*x+phi2)
y1==y2且y1'=y2'
"""
s = "1 7 1 7 1 7 1 7 1 7 1 7 1 7 1 7"
rate = 8000
book = mp.nmn.content2book(s, 0.3)
a = []
phi = 0
for freq, duration in book:
    a.append(mp.nmn.freq2wave(freq, rate, duration, phi=phi, freq_wav_type=mp.nmn.FreqWaveType.constant))
    phi += freq * np.pi * 2 * duration
a = np.concatenate(a)
print(a.dtype)
mp.write('a.wav', a, rate)
mp.play("a.wav")
