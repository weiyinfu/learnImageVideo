"""

8bit音乐：模拟过去的音乐
"""

import numpy as np

import mediapy as mp

meta, audio = mp.read("./taylor.mp3")
print(meta)
print(audio.shape)
downsample_count = 8
audio8bit = np.round(audio[:, 0] / (2 ** 15) * downsample_count)
audio16bit = np.array(audio8bit / downsample_count * 2 ** 15, dtype=np.int16)
mp.write('./taylor8bit.mp3', audio16bit, meta.sample_rate())
