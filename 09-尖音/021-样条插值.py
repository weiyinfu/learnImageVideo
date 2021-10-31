import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate as interpolate

"""
样条插值：给定若干个点，求t，c，k。样条能够将这些点统统连起来。
"""
x = np.array([0., 1.2, 1.9, 3.2, 4., 6.5])
y = np.array([0., 2.3, 3., 4.3, 2.9, 3.1])

t, c, k = interpolate.splrep(x, y, s=0, k=4)
print(f'''
t: {t}
c: {c}
k: {k}
t.shape={t.shape} x.shape={x.shape} y.shape={y.shape}
''')
N = 100
xmin, xmax = np.min(x), np.max(x)
xx = np.linspace(xmin, xmax, N)
spline = interpolate.BSpline(t, c, k, extrapolate=False)

plt.plot(x, y, 'bo', label='Original points')
plt.plot(xx, spline(xx), 'r', label='BSpline')
plt.grid()
plt.legend(loc='best')
plt.show()
