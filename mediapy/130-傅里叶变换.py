import numpy as np

"""
傅里叶变换的本质：计算一个函数在另一个函数上的投影

给定浮点数组a,长度为n，计算它在sin(2pi/n*x),sin(2pi/n*2*x),sin(2pi/n*3*x)...和cos(2pi/n*x),cos(2pi/n*2*x)等每个曲线上的投影。  

傅里叶逆变换：已知基向量x1，x2，坐标为m1,m2，则(x1*m1+x2*m2)
"""
a = np.array([1, 3, 2, 4, 5])
x = np.arange(len(a))
b = np.fft.fft(a)
print(b)
sin_list = []
for i in range(len(a)):
    si = np.sum(np.sin(2 * np.pi / len(a) * i * x) * a)
    sin_list.append(si)
cos_list = []
for i in range(len(a)):
    co = np.sum(np.cos(2 * np.pi / len(a) * i * x) * a)
    cos_list.append(co)
sin_list = np.array(sin_list)
cos_list = np.array(cos_list)
"""
表达形式一：两个数组
"""
print(sin_list)
print(cos_list)
print('============')
"""
表达形式二：一个复数数组
"""
print(cos_list - 1j * sin_list)
print('============')
"""
表达形式三：sin函数+相位
A1*sin(wx)+A2*cos(wx)=Asin(wx+phi)，其中A等于sqrt(A1**2+A2**2)
alpha=arctan2(A1,A2)
phi=-alpha
"""
print(np.angle(b), np.abs(b))
print(-np.arctan2(sin_list, cos_list), np.hypot(sin_list, cos_list))
print("=============")
"""
抛弃变换，直接考虑波形，傅里叶还是非常容易理解的
直接用波形进行表示，就不存在变换的说法了。  
"""
A = np.hypot(sin_list, cos_list)
phi = np.arctan2(cos_list, sin_list)
s = 0
print(A, phi)
for i in range(len(a)):
    s = s + A[i] * np.sin(np.pi * 2 / len(a) * i * x + phi[i])
print(s / len(a))
print("==========")
# 全部化为余弦形式，这也是傅里叶变换中的angle
A = np.hypot(sin_list, cos_list)
phi = np.arctan2(sin_list, cos_list)
s = 0
print(A, phi)
for i in range(len(a)):
    s = s + A[i] * np.cos(np.pi * 2 / len(a) * i * x - phi[i])
print(s / len(a))
print("==========")
s = 0
for i in range(len(a)):
    s = s + sin_list[i] * np.sin(2 * np.pi / len(a) * i * x)
for i in range(len(a)):
    s = s + cos_list[i] * np.cos(2 * np.pi / len(a) * i * x)
print(s / len(a))
print("==========")
