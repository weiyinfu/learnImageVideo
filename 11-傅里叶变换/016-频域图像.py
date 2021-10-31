import numpy as np

import mediapy as mp
import pylab as plt

"""
傅里叶变换之后可以找到5 6 7 1^ 2^ 3^ 4^ 5^共8个音调
"""
# 生日快乐歌
birthday = """
5 5 6 5 1^ 7
5 5 6 5 2^ 1^
5 5 5^ 3^ 1^ 7 6
4^ 4^ 3^ 1^ 2^ 1^ 1^
"""
rate, a = mp.nmn.get_float_array(birthday, rate=10000)
print(a.shape)
b = np.fft.fft(a)
A = np.abs(b)
T = len(a) / rate
print(T)
f = np.arange(len(a)) / len(a) * rate
"""
寻找极值点
"""
window = 50
good = []
for i in range(window, len(A) // 2):
    if np.max(A[i - window:i + window]) == A[i]:
        good.append(i)

print(f[good], len(good))
print(mp.nmn.ma)
plt.plot(f, A)
plt.xlim(0, 1000)
plt.show()
"""
可以发现频谱集中在8个音调上
"""