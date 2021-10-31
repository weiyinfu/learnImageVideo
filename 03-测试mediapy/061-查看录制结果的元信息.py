import mediapy as mp

meta, a = mp.read('a.matroska')
print(meta.video_stream)
print(len(a) / meta.frame_rate(), meta.frame_rate(), '时长')
print(a.shape)
