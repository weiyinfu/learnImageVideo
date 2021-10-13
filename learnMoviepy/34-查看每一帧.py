import math
from os.path import *

import pylab as plt
from skvideo import io

filepath = join(dirname(__file__), "../imgs/delicious.gif")
a = io.vread(filepath)

rows = round(a.shape[0] ** 0.5)
cols = math.ceil(a.shape[0] / rows)

fig, axes = plt.subplots(rows, cols)
axes = axes.reshape(-1)
for i in range(len(a)):
    img = a[i]
    ax = axes[i]
    ax.imshow(img)
    ax.axis('off')
    ax.set_title(f"{i}")
plt.show()
