import numpy as np
from skimage import io

from mediapy import hand
import mediapy as mp

# me = io.imread("../imgs/简笔画/me.jpg")
me = io.imread("yu.jpg")
img = hand.generate_simple_image(me)
import pylab as plt

plt.imshow(img)
plt.show()
ind = np.argwhere(img < 220)
print(img.shape, img.dtype, img.min(), img.max())
print(ind.shape, np.prod(img.shape))
# exit()
xs, ys = ind[:, 0], ind[:, 1]
point_list = hand.analyze_point_sequence(xs, ys)
a = hand.draw_point_list(img, point_list, hand.hands[0][0], hand.hands[0][1])
print(a.shape, a.dtype)
mp.write('a.mp4', a[::3], 20)
mp.play('a.mp4')
