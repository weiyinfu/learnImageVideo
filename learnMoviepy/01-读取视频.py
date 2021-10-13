import skvideo.datasets as d
from moviepy.editor import *

a = VideoFileClip(d.bigbuckbunny())

print("属性列表")
for i in dir(a):
    if i.startswith("_"):
        continue
    v = getattr(a, i)
    if callable(v):
        continue
    print(i, v)
if a.audio:
    print('音频信息')
    for i in dir(a.audio):
        if i.startswith("_"):
            continue
        v = getattr(a.audio, i)
        if callable(v):
            continue
        print(i, v)
