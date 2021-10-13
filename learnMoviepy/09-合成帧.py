import moviepy.editor as e
import skimage.data as d
from moviepy.editor import *

clip1 = e.ImageClip(d.astronaut(), duration=1)
clip2 = e.ImageClip(d.coffee(), duration=1)
clip3 = e.ImageClip(d.rocket(), duration=1)
# 设置每一帧的开始时间
video = CompositeVideoClip([clip1.set_duration(3),  # starts at t=0
                            clip2.set_duration(6).set_start(3),  # start at t=5s
                            clip3.set_duration(9).set_start(6).set_end(9)])  # start at t=9s
video.fps = 1
video.write_videofile("简单拼接.mp4")
# 添加特效
video = CompositeVideoClip([clip1.set_duration(5).crossfadein(2).crossfadeout(2),  # starts at t=0
                            clip2.set_duration(5).set_start(5).crossfadein(3).crossfadeout(3),
                            clip3.set_duration(5).set_start(10).crossfadein(3).crossfadeout(3)])
video.fps = 1
video.write_videofile("渐变拼接.mp4")
# 设置每个片段的位置
video = CompositeVideoClip([clip1,
                            clip2.set_position((45, 150)),
                            clip3.set_position((90, 100))])
video.fps = 1
video.write_videofile("不同位置合成.mp4")

# 设置位置有很多种方法，如果不保存，则不会生效。以下代码仅用于演示
clip2.set_position((45, 150))  # x=45, y=150 , in pixels
clip2.set_position("center")  # automatically centered

# clip2 is horizontally centered, and at the top of the picture
clip2.set_position(("center", "top"))

# clip2 is vertically centered, at the left of the picture
clip2.set_position(("left", "center"))

# clip2 is at 40% of the width, 70% of the height of the screen:
clip2.set_position((0.4, 0.7), relative=True)

# clip2's position is horizontally centered, and moving down !
clip2.set_position(lambda t: ('center', 50 + t))
