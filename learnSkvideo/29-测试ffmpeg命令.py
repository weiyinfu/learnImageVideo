import subprocess as sp

import numpy as np

import skvideo.io as io
from skvideo.datasets import bigbuckbunny

filepath = bigbuckbunny()
a = ['ffmpeg', '-i', filepath, '-f', 'image2pipe', '-pix_fmt', 'rgba', '-vcodec', 'rawvideo', '-']
resp = sp.check_output(a)
print(type(resp))
print(' '.join(a))

dd = io.vread(filepath)
v = np.frombuffer(resp, dtype=np.uint8)
print(v.shape)
print(dd.shape)
print(np.prod(dd.shape))
vv = v.reshape(list(dd.shape[:3]) + [4])
print(np.all(vv[:, :, :, :3] == dd))
