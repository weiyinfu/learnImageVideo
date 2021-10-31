import mediapy as mp

meta, a = mp.read('a.matroska')
print(meta, a.shape)
