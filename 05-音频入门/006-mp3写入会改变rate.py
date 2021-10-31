import numpy as np
import mediapy as mp
"""
mp3是一种有损压缩的数据格式，把数据写进去之后再读出来数据就会发生变化。  

例如，本例中rate会发生改变。而wav格式则一切正常。
"""
a = np.arange(-2 ** 15, 2 ** 15).astype(np.int16)

mp.write('a.wav', a, 21000)
meta = mp.get_meta('a.wav')
print(meta.sample_rate())

mp.write('a.mp3', a, 21000)
meta = mp.get_meta('a.mp3')
print(meta.sample_rate())
