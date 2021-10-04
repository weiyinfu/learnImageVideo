from moviepy import editor

p = "/home/weiyinfu/Videos/为了你.mp4"

video = editor.VideoFileClip(p)
video.audio.write_audiofile('foryou.mp3')
