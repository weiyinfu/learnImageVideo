import subprocess as sp
from io import BytesIO

import numpy as np
import scipy.io.wavfile as wav

filepath = "../imgs/taylor.mp4"
a = ['ffmpeg', '-i', filepath, '-f', 'wav', '-']
resp = sp.check_output(a)
print(type(resp))
print(' '.join(a))
v = np.frombuffer(resp, dtype=np.uint8)
print(v.shape)
rate, data = wav.read(BytesIO(resp))
print(data.shape, data.dtype, rate)
print(data[:10])


def play2():
    _ = sp.check_output(["ffplay", "-"], stdin=open("a.wav", "rb"))


def play1():
    x = sp.Popen(['ffplay', '-'], stdin=sp.PIPE)
    x.stdin.write(resp)
    x.wait(1000)
