import numpy as np

rate = 8000
a = np.random.random((rate * 10)) * 255
b = np.random.randint(-2 ** 15, 2 ** 15 - 1, (rate * 10), dtype=np.int16)
print(a.dtype, a.shape)
import mediapy as mp

# mp.write('a.mp3', a, rate)
# mp.play('a.mp3')
mp.write('b.mp3', b, rate)
mp.play('b.mp3')
