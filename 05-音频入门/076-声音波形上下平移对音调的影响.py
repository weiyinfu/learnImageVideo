import mediapy as mp
import numpy as np

meta, a = mp.read('../imgs/taylor.mp3')

print(a.shape)
print(np.mean(a), np.median(a), np.min(a), np.max(a))
a = a + 8000
mp.write('b.mp3', a, meta.sample_rate())
mp.play('b.mp3')
