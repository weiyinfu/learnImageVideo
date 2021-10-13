import subprocess as sp

import numpy as np

filepath = "../imgs/taylor.mp4"
a = ['ffmpeg', '-i', filepath, '-f', 's16le', '-']
resp = sp.check_output(a)
print(type(resp))
print(' '.join(a))
v = np.frombuffer(resp, dtype=np.int16)
v = v.reshape(-1, 2)
print(v.shape, v.dtype)
print(v[:10])
print(np.count_nonzero(v < 0))
"""
(9856000, 2) int16
[[203 203]
 [599 599]
 [795 795]
 [704 704]
 [646 646]
 [655 655]
"""
