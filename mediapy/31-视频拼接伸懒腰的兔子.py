"""
把两个视频拼接起来
bigbuckbunny是一个动画片，一只兔子从洞里出来，伸了伸懒腰。
此程序把这个片段倒转过来。实际效果就是：兔子从动力出来，又回去了。
"""
import numpy as np
import skvideo.datasets as d

import mediapy as mp

meta, a = mp.read(d.bigbuckbunny())
b = np.concatenate([a, a[::-1, :, :, :]])
print(a.shape, b.shape)
mp.write("a.mp4", np.concatenate([b, b, b, b]), rate=meta.video_stream.r_frame_rate)
