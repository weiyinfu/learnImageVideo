"""
一个手电筒照在一张大图片上，手电筒外面是黑色的，只有手电筒部分可见
"""
import numpy as np
from skimage import io, draw as dr
from tqdm import tqdm

import mediapy as mp

img = io.imread("../imgs/2.jpg")

video = np.zeros((1000, *img.shape), dtype=np.uint8)
x, y = img.shape[0] / 2, img.shape[1] / 2
r = 150
v = 10
theta = np.pi * 2 * np.random.random()
for i in tqdm(range(video.shape[0])):
    xx, yy = dr.circle(x, y, r)
    good = np.argwhere(np.logical_and(np.logical_and(xx >= 0, xx < img.shape[0]), np.logical_and(yy >= 0, yy < img.shape[1])))
    video[i, xx[good], yy[good]] = img[xx[good], yy[good]]
    if x < 20 or x > img.shape[0] - 20 or y < 20 or y > img.shape[1] - 20:
        dy, dx = img.shape[1] / 2 - y, img.shape[0] / 2 - x
        theta = np.arctan2(dy, dx)
    else:
        if i % 120 == 0:
            theta = np.random.random() * np.pi * 2
    dx, dy = v * np.cos(theta), v * np.sin(theta)
    x = x + dx
    y = y + dy

print(video.shape)
mp.write("a.mp4", video, rate=20)
song = """
3 5 5 6 5 3 1  1 2 3 3 2 1 2
3 5 5 6 5 3 1  1 2 3 3 2 2 1
4 4 4 6  5 5 3 2
3 5 5 6 5 3 1  1 2 3 3 2 2 1 
"""
mp.nmn.build_music("a.wav", song, 8000)
mp.combine('b.mp4', 'a.mp4', 'a.wav', audio_loop=-1)
mp.play('b.mp4')
