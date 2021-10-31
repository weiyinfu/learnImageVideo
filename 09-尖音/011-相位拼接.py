import numpy as np
import pylab as plt

"""
相位拼接的要点：y1=Asin(w1*x+phi1),y2=Bsin(w2*x+phi2)
y1==y2且y1'=y2'，这其实就是光滑的定义

前一段为A1sin(w1*x+phi1)
后一段为A2sin(w2*x+phi2)

w1*x+phi1=w2*x+phi2，满足这个公式就能够保证平滑，这就是相位拼接的原理
"""
x = np.linspace(0, 3, 100)
y1 = np.sin(x[:len(x) // 2])
t = x[len(x) // 2 - 1]
tt = x[len(x) // 2]
phi = t - 2 * t
y2 = np.sin(2 * x[len(x) // 2:] + phi)
y = np.concatenate([y1, y2])
plt.plot(x, y)
plt.vlines(x[len(x) // 2], y.min(), y.max())
plt.show()
