import numpy as np
from tqdm import tqdm

import mediapy as mp

"""
七种颜色组成一个旋转盘，旋转盘越转越快，验证最终是否会kan
"""
sz = 700
img = np.zeros((sz, sz, 3), dtype=np.uint8)
colors = np.array([
    [255, 0, 0],
    [255, 165, 0],
    [255, 255, 0],
    [0, 255, 0],
    [0, 127, 255],
    [0, 0, 255],
    [139, 0, 255],
])
center = np.array(img.shape[:2]) / 2
x, y = np.mgrid[:img.shape[0], :img.shape[1]]
xy = np.dstack([x, y])
dis2center = np.linalg.norm(xy - center, axis=2)
theta = np.arctan2(y - center[1], x - center[0])
good_ind = dis2center < sz * 0.45
import pylab as plt


def get_image(alpha):
    img = np.zeros((sz, sz, 3), dtype=np.uint8)
    color_index = colors[np.array(((theta + alpha) // (np.pi * 2 / len(colors)) + len(colors)) % len(colors), dtype=np.int)]
    img[good_ind] = color_index[good_ind]
    return img


def show():
    img = get_image(0)
    plt.imshow(img)
    plt.show()


speed = np.linspace(np.pi / 30, np.pi / 2, 500)
speed = np.repeat(speed, 10)
pos = np.cumsum(speed)
a = []
for i in tqdm(range(pos.shape[0]), desc='正在生成视频'):
    now = get_image(pos[i])
    a.append(now)
a = np.array(a)
mp.write('a.mp4', a, rate=50)
mp.play('a.mp4')
