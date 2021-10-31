import mediapy as mp

import numpy as np

number = []
for i in range(10):
    filepath = f"../数字语音朗读器/res/{i}.wav"
    meta, audio = mp.read(filepath)
    number.append((meta, audio.reshape(-1)))
s = "18810952023"

print(number[0][1].dtype, number[0][1].shape)


def text2fragment(s: str):
    return [number[int(i)][1] for i in s]


def direct_concate(a):
    return np.concatenate(a)


frags = text2fragment(s)
b = direct_concate(frags)
mp.write('a.mp3', b, rate=number[0][0].sample_rate())
mp.play('a.mp3')
