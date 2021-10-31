import numpy as np
"""
回忆一下小时候电视收不到台的景象
"""
duration = 10
sample_rate = 8000
b = np.random.randint(-2 ** 15, 2 ** 15 - 1, (sample_rate * duration), dtype=np.int16)
frame_rate = 20
a = (np.random.random((frame_rate * duration, 500, 500, 3)) * 255).astype(np.uint8)
import mediapy as mp

mp.write('a.mp4', a, frame_rate)
mp.write('a.mp3', b, sample_rate)
mp.combine('b.mp4', 'a.mp4', 'a.mp3')
mp.play('b.mp4')
