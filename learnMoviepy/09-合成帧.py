import moviepy.editor as e
import skimage.data as d
from moviepy.editor import CompositeVideoClip

clip1 = e.ImageClip(d.astronaut())
clip2 = e.ImageClip(d.coffee())
clip3 = e.ImageClip(d.rocket())
final_clip = CompositeVideoClip([clip1, clip2, clip3], size=(720, 460))
final_clip = final_clip.set_duration(3)
final_clip = final_clip.set_fps(1)
print(final_clip.duration)
final_clip.write_gif("haha.gif")
#
# # 设置每一帧的开始时间
# video = CompositeVideoClip([clip1,  # starts at t=0
#                             clip2.set_start(5),  # start at t=5s
#                             clip3.set_start(9)])  # start at t=9s
#
# # 添加特效
# video = CompositeVideoClip([clip1,  # starts at t=0
#                             clip2.set_start(5).crossfadein(1),
#                             clip3.set_start(9).crossfadein(1.5)])
#
# # 设置每个片段的位置
# video = CompositeVideoClip([clip1,
#                             clip2.set_position((45, 150)),
#                             clip3.set_position((90, 100))])
#
# # 设置位置有很多种方法
# clip2.set_position((45, 150))  # x=45, y=150 , in pixels
#
# clip2.set_position("center")  # automatically centered
#
# # clip2 is horizontally centered, and at the top of the picture
# clip2.set_position(("center", "top"))
#
# # clip2 is vertically centered, at the left of the picture
# clip2.set_position(("left", "center"))
#
# # clip2 is at 40% of the width, 70% of the height of the screen:
# clip2.set_position((0.4, 0.7), relative=True)
#
# # clip2's position is horizontally centered, and moving down !
# clip2.set_position(lambda t: ('center', 50 + t))
