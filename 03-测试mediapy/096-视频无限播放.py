import mediapy as mp

# mp.play('../imgs/taylor.mp4')
meta, a = mp.read('../imgs/taylor.mp4')
print(a.shape, a.dtype)
print(meta.video_stream)
writer = mp.get_writer(a.dtype, a.shape[1:], mp.matroska, rate=meta.frame_rate(), media_type=mp.MediaType.video)

mp.play_pipe(writer)
i = 0
while 1:
    print(f"writing {i}")
    i += 1
    writer.write(a)
    print('sleep over')
writer.cin.close()
