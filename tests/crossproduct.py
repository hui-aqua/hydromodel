import numpy as np

u = np.array([1, 0, 0])
n = np.array([1, 1, 1] / np.sqrt(3))

c1 = np.cross(u, n)
c2 = np.cross(c1, u)
