"""
给定文本让手产生写字的视频
给定一张图片，让手产生画画的视频
给定一个文字，求文字的笔顺。

查看各个hand图片
"""
import os

import pylab as plt
from skimage import io

hand_folder = "../imgs/hand"
print(os.listdir(hand_folder))
for i in os.listdir(hand_folder):
    img = io.imread(f"../imgs/hand/{i}")
    plt.imshow(img)
    plt.show()
