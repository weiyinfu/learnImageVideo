import numpy as np

import mediapy as mp

"""
float格式的音频数值上不能超过1，超过1就会强制写成1. 
"""

a = np.random.random(100000) * 3 - 1.5

mp.write('a.wav', a, 21000)
meta = mp.get_meta('a.wav')
print('sample_rate', meta.sample_rate())


def float2float():
    meta, b = mp.read('a.wav', out_audio_fmt=mp.AudioFormat.f32le)
    print('shape', a.shape, b.shape)
    print('dtype', a.dtype, b.dtype)
    b = b.reshape(-1)
    print(np.max(b), np.min(b))
    print(np.allclose(a, b, atol=1e-4))


def float2int():
    for i in (mp.AudioFormat.s16be, mp.AudioFormat.s32be):
        meta, b = mp.read('a.wav', out_audio_fmt=i)
        print('shape', a.shape, b.shape)
        print('dtype', a.dtype, b.dtype)
        b = b.reshape(-1)
        print(i, np.mean(b / a))


float2float()
