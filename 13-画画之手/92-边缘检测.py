import numpy as np
import pylab as plt
from skimage import color, io, filters

me = io.imread("./me.jpg")
me = color.rgb2grey(me)
print(me.shape, me.dtype)
img = filters.sobel(me)
plt.imshow(1 - img, plt.cm.gray)
plt.show()
