import time

import matplotlib.pyplot as plt

import mediapy as mp
import skvideo.io as vio
from skvideo.datasets import bigbuckbunny

filepath = bigbuckbunny()
t1 = time.time()
meta, data = mp.read(filepath)
t2 = time.time()
print("mine", t2 - t1)
data2 = vio.vread(filepath, verbosity=True)
print("his", time.time() - t2)
print(data.dtype, data.shape)
print(data2.dtype, data2.shape)
print(meta.video_stream)
cnt = 5
fig, axes = plt.subplots(cnt, 2)
for i in range(cnt):
    x, y = data[i], data2[i]
    xx, yy = axes[i]
    xx.imshow(x)
    yy.imshow(y)
plt.show()
