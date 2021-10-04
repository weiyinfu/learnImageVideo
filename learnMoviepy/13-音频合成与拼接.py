# ... make some audio clips aclip1, aclip2, aclip3
import os
from os.path import *

from moviepy import editor as e

"""
实际上合成包括拼接
"""
h = os.path.expanduser("~")
filepath = join(h, "Music/故乡的原风景.mp3")
a = e.AudioFileClip(filepath)
print(dir(a))
one = a.subclip(0, 10)
two = a.subclip(20, 30)
three = a.subclip(40, 50)
# 拼接
concat = e.concatenate_audioclips([one, two, three])
sound = e.CompositeAudioClip([one.volumex(1.2), two.set_start(5), three.set_start(8)]).set_fps(a.fps)
sound.write_audiofile("composite.mp3")
concat.write_audiofile("concate.mp3")
