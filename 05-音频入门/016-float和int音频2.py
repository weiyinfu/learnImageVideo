import numpy as np

import mediapy as mp

"""
音频有float和int两种表示形式，int都是带符号的。
float*max positive int=int
例如float32格式的音频都是0到1之间的数值，乘以32768（2**15）便得到s16格式的音频
"""

a = np.arange(-2 ** 15, 2 ** 15).astype(np.int16)

mp.write('a.wav', a, 21000)
meta = mp.get_meta('a.wav')
print('sample_rate', meta.sample_rate())
meta, b = mp.read('a.wav', out_audio_fmt=mp.AudioFormat.f64le)
print('shape', a.shape, b.shape)
print('dtype', a.dtype, b.dtype)
b = b.reshape(-1)
c = a.astype(np.float) / (b + 1e-10)
print('c', np.min(c), np.max(c), np.mean(c))
print('b', np.min(b), np.max(b), np.mean(b))
print(2 ** 15)
