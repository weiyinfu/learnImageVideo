import numpy as np

import mediapy as mp

"""
音频有float和int两种表示形式，int都是带符号的。
float*(最大正数)=int
例如float32格式的音频都是0到1之间的数值，乘以32768（2**15）便得到s16格式的音频
"""

a = np.random.random(100000)

mp.write('a.wav', a, 21000)
meta = mp.get_meta('a.wav')
print('sample_rate', meta.sample_rate())


def float2float():
    meta, b = mp.read('a.wav', out_audio_fmt=mp.AudioFormat.f64le)
    print('shape', a.shape, b.shape)
    print('dtype', a.dtype, b.dtype)
    b = b.reshape(-1)
    print(np.allclose(a, b, atol=1e-4))


def float2int():
    for i in (mp.AudioFormat.s16be, mp.AudioFormat.s32be):
        meta, b = mp.read('a.wav', out_audio_fmt=i)
        print('shape', a.shape, b.shape)
        print('dtype', a.dtype, b.dtype)
        b = b.reshape(-1)
        print(i, np.mean(b / a))


float2int()
