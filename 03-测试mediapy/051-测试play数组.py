import time

import mediapy as mp

meta, audio = mp.read("../imgs/taylor.mp3")
writer = mp.get_writer('-', audio.dtype, audio.shape[1:], "mp3", meta.sample_rate(), 'audio')
p = mp.play_pipe(writer)
time.sleep(10)
writer.write(audio[:len(audio) // 2])
print("writed half")
# time.sleep(20) # 如果中间停了就会停止播放了
print("asdfasdf")
writer.write(audio[len(audio) // 2:])
print("asdfasdf=====")
writer.cin.close()
# print(writer.cin.closed)
p.join()
