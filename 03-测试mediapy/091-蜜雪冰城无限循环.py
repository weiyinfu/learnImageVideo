import mediapy as mp

# 蜜雪冰城
mixuebingcheng = """
3 5 5 6 5 3 1  1 2 3 3 2 1 2
3 5 5 6 5 3 1  1 2 3 3 2 2 1
4 4 4 6  5 5 3 2
3 5 5 6 5 3 1  1 2 3 3 2 2 1 
"""
rate, a = mp.nmn.get_float_array(mixuebingcheng, rate=8000, space_seconds=0.3, freq_wav_type=mp.nmn.FreqWaveType.three)
writer = mp.get_writer('-', a.dtype, 1, 'mp3', rate=rate, media_type=mp.MediaType.audio)
mp.play_pipe(writer)
i = 0
while 1:
    print(f"writing {i}")
    i += 1
    writer.write(a)
    """
    此处实际上不需要sleep，因为写缓存区满了之后自然而然就会发生写阻塞
    """
writer.cin.close()
