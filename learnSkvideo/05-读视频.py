import numpy as np
from skvideo import datasets as d
from skvideo import io

"""
读取视频数据的三种写法：
* 第一种写法：一次性加载到内存
* 第二种写法：vreader，以迭代器的形式获取每一帧的数据
* 第三种写法：FFMpegReader，这种写法更为底层，也更为灵活
"""
bikes = io.vread(d.bikes(), verbosity=1)
print(bikes.shape, type(bikes))

# 以迭代器的形式读取视频，避免视频太大
videogen = io.vreader(d.bigbuckbunny(), verbosity=1)
for frame in videogen:
    print(frame.shape)

# set keys and values for parameters in ffmpeg
"""
使用inputparameters和outputparameters可以向ffmpeg传入一些特殊的命令
"""
inputparameters = {}
outputparameters = {}
reader = io.FFmpegReader(d.bigbuckbunny(),
                         inputdict=inputparameters,
                         outputdict=outputparameters)
print(inputparameters)
print(outputparameters)
# iterate through the frames
accumulation = 0
for frame in reader.nextFrame():
    # do something with the ndarray frame
    print(frame.shape)
    accumulation += np.sum(frame)
