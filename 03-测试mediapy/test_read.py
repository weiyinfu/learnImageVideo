import numpy as np
import scipy.io.wavfile as wav

import mediapy as mp

"""
与scipy进行比较，证明mediapy正确
"""


def test_audio():
    meta, data = mp.read("../imgs/taylor.wav")
    _, data2 = wav.read("../imgs/taylor.wav")
    print(data.shape, data2.shape)
    print(data.dtype, data2.dtype)
    print(np.all(data == data2))


def test_video():
    meta, a = mp.read('a.matroska')
    print(meta, a.shape)
