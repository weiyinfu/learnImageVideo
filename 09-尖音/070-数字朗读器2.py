import pylab as plt

import mediapy as mp

"""
缺点是一旦断流就不在响了
"""
number = []
for i in range(10):
    filepath = f"../数字语音朗读器/res/{i}.wav"
    meta, audio = mp.read(filepath)
    number.append((meta, audio.reshape(-1)))
zero = number[0]
writer = mp.get_writer('-', zero[1].dtype, 1, 'wav', rate=zero[0].sample_rate(), media_type=mp.MediaType.audio)
mp.play_pipe(writer)


def on_cmd(cmd):
    print(cmd.key)
    s = cmd.key
    if s in '0123456789' and len(s):
        m, v = number[int(s)]
        print(s, v.shape)
        writer.write(v)


fig, axes = plt.subplots(figsize=(8, 8), facecolor='black')
fig.canvas.mpl_connect('key_press_event', on_cmd)
plt.show()
