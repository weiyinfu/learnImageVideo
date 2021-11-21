import numpy as np

"""
空间几何中角度与其投影的关系

一个角度分解成alpha、beta、gamma三个角度
"""
a, b = np.random.random((2, 3))


def get_angle(a, b):
    cosx = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    angle = np.arccos(cosx)
    return angle


A = get_angle(a, b)
x = get_angle([a[0], a[1]], [b[0], b[1]])
y = get_angle([a[0], a[2]], [b[0], b[2]])
z = get_angle([a[2], a[1]], [b[2], b[1]])
print(A, x, y, z)
print(np.cos(A) ** 2, np.sum(np.cos([x, y, z]) ** 2) / 3)
