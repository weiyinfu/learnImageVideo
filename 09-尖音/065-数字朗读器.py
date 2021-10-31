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
i = 0
while 1:
    print(f"writing {i}")
    i += 1
    s = input('input number').strip()
    if s in '0123456789' and len(s):
        m, v = number[int(s)]
        print(s, v.shape)
        for j in range(10):
            writer.write(v)
