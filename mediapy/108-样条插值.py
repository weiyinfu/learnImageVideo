import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate as interpolate

x = np.array([0., 1.2, 1.9, 3.2, 4., 6.5])
y = np.array([0., 2.3, 3., 4.3, 2.9, 3.1])

t, c, k = interpolate.splrep(x, y, s=0, k=4)
print('''\
t: {}
c: {}
k: {}
'''.format(t, c, k))
N = 100
xmin, xmax = np.min(x), np.max(x)
xx = np.linspace(xmin, xmax, N)
spline = interpolate.BSpline(t, c, k, extrapolate=False)

plt.plot(x, y, 'bo', label='Original points')
plt.plot(xx, spline(xx), 'r', label='BSpline')
plt.grid()
plt.legend(loc='best')
plt.show()
