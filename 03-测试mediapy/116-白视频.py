import numpy as np

rate = 20
a = (np.random.random((200, 500, 500, 3)) * 255).astype(np.uint8)
print(a.dtype, a.shape)
import mediapy as mp

mp.write('a.mp4', a, rate)
mp.play('a.mp4')
