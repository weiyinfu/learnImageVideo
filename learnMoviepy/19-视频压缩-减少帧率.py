from moviepy.editor import *

from skvideo import datasets as d

a = d.bikes()
a = VideoFileClip(a)
print(a.duration, a.fps)
sz = int(a.duration * a.fps)
b = [a.get_frame() for i in range(0, sz, 2)]

c = concatenate_videoclips(b)
c.fps = int(a.fps / 2)
c.write_videofile("bike.mp4")
