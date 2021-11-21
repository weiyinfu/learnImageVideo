import numpy as np

a = np.random.random((3, 3, 2))
b = np.random.random((2, 2))
c = np.matmul(a, b)
print(c.shape)
