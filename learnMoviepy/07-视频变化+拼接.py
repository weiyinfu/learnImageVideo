from moviepy.editor import VideoFileClip, clips_array, vfx
from skvideo.datasets import bigbuckbunny

"""
最终产生一个两行两列的视频，第一个是原画，第二个是水平镜像，第三个是竖直镜像，第四个是缩小
"""
clip1 = VideoFileClip(bigbuckbunny()).margin(10)  # add 10px contour
clip2 = clip1.fx(vfx.mirror_x)
clip3 = clip1.fx(vfx.mirror_y)
clip4 = clip1.resize(0.60)  # downsize 60%
final_clip = clips_array([[clip1, clip2],
                          [clip3, clip4]])
final_clip.resize(width=480).write_videofile("bigbuckbunny.mp4")
