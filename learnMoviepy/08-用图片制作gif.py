import moviepy.editor as e
import skimage.data as d

clip1 = e.ImageClip(d.astronaut(), duration=1)
clip2 = e.ImageClip(d.coffee(), duration=1)
clip3 = e.ImageClip(d.rocket(), duration=1)
final_clip = e.concatenate_videoclips([clip1, clip2, clip3])
final_clip = final_clip.set_duration(3)
final_clip = final_clip.set_fps(1)
print(final_clip.duration)
final_clip.write_gif("haha.gif")
