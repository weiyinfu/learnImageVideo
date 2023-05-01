import numpy as np

import mediapy as mp

"""
使用这种网状结构，非常容易确认VR视频是如何渲染的 
"""

thick = 3
color = (200, 0, 0)
a = np.ndarray((20 * 10, 700, 1400, 3), dtype=np.uint8)
for i in range(0, a.shape[1], 100):
    a[:, i:i + thick, :] = color
for i in range(0, a.shape[2], 100):
    a[:, :, i:i + thick] = color

mp.write('a.mp4', a, rate=20)
mp.change_format('a.mp4', 'b.mp4', 'yuv420p')
