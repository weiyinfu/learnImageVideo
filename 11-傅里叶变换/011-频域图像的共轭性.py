import numpy as np
"""
傅里叶变换把n个浮点数变成了2n个浮点数，这岂不是违背了压缩定律，数字为啥变多了？

实际上没有变多，当n为偶数的时候
0和n//2的虚部为0，剩余的数字为共轭。
当n为奇数的时候，以第一个数字为中心正好划分为两半。
"""
a = np.arange(6)
print(a.shape)
b = np.fft.fft(a)
if len(a) & 1:
    l, r = b[1:len(b) // 2 + 1], b[-len(b) // 2 + 1:]
    print(np.allclose(np.conj(l), r[::-1]))
else:
    print(b)
    l, r = b[1:len(b) // 2], b[-len(b) // 2 + 1:]
    print(np.allclose(np.conj(l), r[::-1]))
