import mediapy as mp
from skvideo.datasets import bigbuckbunny

filepath = bigbuckbunny()
meta, a = mp.read(filepath)
mp.write('a.mp4', a, meta.frame_rate())
"""
ffmpeg -y -f rawvideo -pix_fmt rgb24 -s 680x480 -i - outputvideo.mp4
"""
