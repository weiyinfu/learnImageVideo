import mediapy as mp

meta, a = mp.read("飞书20211113-130054.mp4")
mp.write('a.mp4', a[::-1], meta.frame_rate())
meta, audio = mp.read("飞书20211113-130054.mp4", media_type=mp.MediaType.audio)
mp.write('a.mp3', audio, meta.sample_rate())
mp.combine('b.mp4', 'a.mp4', 'a.mp3', by_video_time=False)
