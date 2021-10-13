from moviepy.editor import *

from skvideo import datasets as d

a = d.bigbuckbunny()
a = VideoFileClip(a)
print(a.duration, a.fps)
sz = round(a.duration * a.fps)
per = 1 / a.fps
b = [ImageClip(a.get_frame(i * per)) for i in range(0, sz, 2)]
for i in b:
    i.duration = a.duration / (sz / 2)
c = concatenate_videoclips(b)
c.fps = int(a.fps / 2)
c.write_videofile("a.mp4")

aa = VideoFileClip(d.bigbuckbunny())
bb = VideoFileClip("a.mp4")
print(aa.duration, bb.duration)
print(aa.fps, bb.fps)
