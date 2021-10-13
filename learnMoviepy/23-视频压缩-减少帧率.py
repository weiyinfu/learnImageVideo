import skvideo.io as vio
from moviepy.editor import VideoFileClip
from skvideo import datasets as d

"""
直接使用skvideo，读一次，写一次即可。
"""
filepath = d.bigbuckbunny()
a = vio.vread(filepath)
metadata = vio.ffprobe(filepath)
r = eval(metadata['video']['@r_frame_rate'])
print('frame_rate', r)


def write1():
    vio.vwrite("a.mp4", a, inputdict={'-r': str(r)}, outputdict={'-r': f"{r / 2}"}, verbosity=1)


def write2():
    # 如果对原数组进行采样，则应该相应地改变采样率
    vio.vwrite("a.mp4", a[::2], inputdict={'-r': str(r / 2)}, outputdict={'-r': f"{r / 2}"}, verbosity=1)


write2()
b = vio.vread("a.mp4")
print(a.shape, b.shape)
b_info = vio.ffprobe("a.mp4")
print(b_info['video']['@r_frame_rate'])
vio.vwrite('original.mp4', a)

aa = VideoFileClip(filepath)
bb = VideoFileClip("a.mp4")
print(aa.duration, bb.duration)
