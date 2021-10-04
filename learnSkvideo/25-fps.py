"""
fps意思是frames perseconds，也就是帧率

无论是音频还是视频，都是离散的东西，把它们快速播放就变成了连续。

总帧数=时长 * 帧率
文件大小=帧数 * 每帧的字节数

对于音频，如果是单轨道，相当于深度为一
如果是双轨道，相当于深度为二

对于视频，如果是灰色，相当于深度为1
如果是三色相当于深度为3

skimage的vwrite默认的帧率是25。
"""
from moviepy import editor
from skvideo import io

a = io.vread("a.mp4")
print(a.shape)
b = editor.VideoFileClip("a.mp4")
print(b.duration)
print(b.fps)
print(b.duration * b.fps)
