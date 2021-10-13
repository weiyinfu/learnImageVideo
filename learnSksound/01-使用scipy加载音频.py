import scipy.io.wavfile as wav

rate, data = wav.read("../imgs/childhood.wav")
print(rate, data.shape)
if len(data.shape) == 1:
    # 如果是一维数组，则直接判定为单通道
    numChannels = 1
    totalSamples = len(data)
else:
    numChannels = data.shape[1]
    totalSamples = data.shape[0]

duration = float(totalSamples) / rate
dataType = str(data.dtype)
print(data.dtype)
# 保存wav文件
# wav.write("childhood.wav",rate,data)
