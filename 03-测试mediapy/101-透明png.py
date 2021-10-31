import numpy as np
from skimage import draw, io

import mediapy as mp
import pylab as plt

"""
透明的png图片并不能在桌面上透明显示
"""
a = np.zeros((100, 100, 4))
a[:] = (0, 125, 0, 50)
x, y = draw.circle(50, 50, 20)
print(x.shape)
print(x)
a[x, y, :] = (125, 0, 0, 125)
print(a[3,3])
plt.imshow(a)
# plt.show()
io.imsave('a.png', a)
mp.play('a.png', auto_exit=False, border_less=True)
