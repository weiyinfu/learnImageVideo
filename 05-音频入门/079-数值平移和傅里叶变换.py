import numpy as np

"""
平移并不影响频率
所以波形其实只是一个数值，真正播放的时候，音调还是不变
"""
a = np.array([1, 3, 2, 4, 5])
b = a + 10
aa = np.fft.fft(a)
bb = np.fft.fft(b)
print(aa)
print(bb)
