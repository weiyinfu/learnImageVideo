import numpy as np
from tqdm import tqdm

import mediapy as mp
import skimage.draw as dr

"""
人类群星闪耀时
"""
a = []
rows = 480
cols = 680
added_circle = []
for i in tqdm(range(300)):
    if np.random.random() < 0.2:
        x, y = np.random.random(2) * np.array([rows, cols])
        r = np.random.random() * 20
        color = np.random.random(3)
        added_circle.append((x, y, r, np.pi * r * r, color))
    now = np.zeros((rows, cols, 3), dtype=np.float32)
    nex = []
    for x, y, r, w, color in added_circle:
        if w / (r * r * np.pi) < 1e-1:
            continue
        nex.append((x, y, r * 1.01, w, color))
        xx, yy = dr.circle(x, y, r)
        good = np.argwhere(np.logical_and(np.logical_and(xx >= 0, xx < rows), np.logical_and(yy >= 0, yy < cols)))
        now[xx[good], yy[good]] += w / (np.pi * r * r) * color
    added_circle = nex
    a.append(now.copy())
a = np.array(np.clip(a, 0, 1) * 255, dtype=np.uint8)
print(a.shape, a.dtype)
mp.write("a.mp4", a, rate=30)
