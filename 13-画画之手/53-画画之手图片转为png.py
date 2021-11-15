"""
给定文本让手产生写字的视频
给定一张图片，让手产生画画的视频
给定一个文字，求文字的笔顺。

查看各个hand图片
"""
import math
import os

import numpy as np
from skimage import io

hand_folder = "../imgs/hand"
print(os.listdir(hand_folder))
image_list = []
filenames = []
for i in os.listdir(hand_folder):
    filenames.append(i)
    img = io.imread(f"../imgs/hand/{i}")
    im = np.zeros(shape=(*img.shape[:2], 4), dtype=img.dtype)
    im[:, :, 3] = 255
    im[:, :, :3] = img
    mean = np.mean(img, axis=2)
    sigma = np.std(img, axis=2)
    ind = np.logical_and(mean > 200, sigma < 3)
    print(ind.shape, np.count_nonzero(ind))
    print(img.shape, mean.shape, sigma.shape)
    im[ind] = 0
    image_list.append(im)
import pylab as plt

rows = int(len(image_list) ** 0.5)
cols = math.ceil(len(image_list) / rows)
fig, axes = plt.subplots(rows, cols)
axes = axes.reshape(-1)[:len(image_list)]
for name, image, axe in zip(filenames, image_list, axes):
    axe.imshow(image)
    axe.set_title(name)
plt.show()
