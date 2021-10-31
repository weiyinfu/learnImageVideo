import pylab as plt

import mediapy as mp

"""
一个简单的朗读器，类似html版
"""
number = []
for i in range(10):
    filepath = f"../数字语音朗读器/res/{i}.wav"
    meta, audio = mp.read(filepath)
    number.append((filepath, meta, audio.reshape(-1)))


def on_cmd(cmd):
    print(cmd.key)
    s = cmd.key
    if s in '0123456789' and len(s):
        mp.play(number[int(s)][0], disable_graphics=1, auto_exit=0)


fig, axes = plt.subplots(figsize=(8, 8), facecolor='black')
fig.canvas.mpl_connect('key_press_event', on_cmd)
plt.show()
