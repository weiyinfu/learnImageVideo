import numpy as np
import skimage.draw as dr

import mediapy as mp

"""
画一个旋转的圆球，圆球动的太快了，就会发现倒转现象
倒转现象是因为达到了人眼的采样率上限
"""
a = []
rate = 200
theta = np.pi * 2 / rate * 16
w, h = 300, 300
R = 80

for i in range(3000):
    img = np.zeros((w, h, 3), dtype=np.uint8)
    the = theta * i
    x, y = dr.circle(w / 2 + R * np.cos(the), h / 2 + R * np.sin(the), 20)
    img[x, y, :] = 254
    a.append(img)
video = np.array(a)
print(video.shape, video.dtype)
mp.write('a.mov', video, rate=rate)
mp.play("a.mov")
