import subprocess as sp
a=['/Users/bytedance/knife-bin/ffmpeg', '-i', '/Users/bytedance/anaconda3/lib/python3.7/site-packages/skvideo/datasets/data/bikes.mp4', '-f', 'image2pipe', '-pix_fmt', 'rgb24', '-vcodec', 'rawvideo', '-']
resp=sp.check_output(a)
print(type(resp))
print(' '.join(a))