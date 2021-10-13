from os.path import *

from moviepy import editor

p = join(expanduser("~"), "Videos/为了你.mp4")
video = editor.VideoFileClip(p)
video.audio.write_audiofile('foryou.mp3')
