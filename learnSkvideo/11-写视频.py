import numpy as np
import skvideo.io

"""
写视频有两种方式：
* 直接vwrite，传入一个帧迭代器
* 使用FFmpegWriter，这是一种更底层的API
"""
outputdata = np.random.random(size=(255, 480, 680, 3)) * 255
outputdata = outputdata.astype(np.uint8)

skvideo.io.vwrite("outputvideo.mp4", outputdata, verbosity=1)

import skvideo.io
import numpy as np

outputdata = np.random.random(size=(225, 480, 680, 3)) * 255
outputdata = outputdata.astype(np.uint8)

writer = skvideo.io.FFmpegWriter("outputvideo2.mp4", outputdict={
    '-vcodec': 'libx264', '-b': '300000000'
})
for i in range(len(outputdata)):
    writer.writeFrame(outputdata[i, :, :, :])
writer.close()
