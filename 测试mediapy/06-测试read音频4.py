import mediapy as mp

xmeta, x = mp.read("./taylor.mp3")
ymeta, y = mp.read("../imgs/taylor.mp3")
print(x.shape, y.shape, x.dtype, y.dtype)
print(xmeta)
print(ymeta)
