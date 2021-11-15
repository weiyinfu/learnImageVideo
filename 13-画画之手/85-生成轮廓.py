import numpy as np
import pylab as plt
from skimage import color, io, measure

me = io.imread("./me.jpg")
me = color.rgb2grey(me)
print(me.shape, me.dtype)
edges = measure.find_contours(me, 0.5)
print(type(edges), len(edges))
img = np.zeros_like(me)
for e in edges:
    e = np.array(e, dtype=np.int32)
    img[e[:, 0], e[:, 1]] = 1
img = 1 - img
plt.imshow(img, plt.cm.gray)
plt.show()
