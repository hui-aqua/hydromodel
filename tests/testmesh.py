import numpy as np
from numpy import pi
import os
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

import matplotlib.pyplot as plt

D = 50.0  # [m]  fish cage diameter

H = 30.0  # [m]  fish cage height
NT = 10  # it can use int(pi*D/L)   # Number of the nodes in circumference
NN = 6  # it can use int(H/L)      # number of section in the height, thus, the nodes should be NN+1
p = []
cagebottomcenter = [0, 0, -1.5 * H]

# generate the point coordinates matrix for the net
for j in range(0, NN + 1):
    for i in range(0, NT):
        p.append([D / 2 * np.cos(i * 2 * pi / float(NT)), D / 2 * np.sin(i * 2 * pi / float(NT)), -j * H / float(NN)])
p.append(cagebottomcenter)

con = []
sur = []
for i in range(1, NT + 1):
    for j in range(0, NN + 1):
        if j == NN:
            con.append([i + j * NT - 1, len(p) - 1])  # add the vertical line into geometry
            if i == NT:
                con.append([i + j * NT - 1, 1 + i + (j - 1) * NT - 1])  # add the horizontal line into geometry
                sur.append([i + j * NT - 1, 1 + i + (j - 1) * NT - 1, len(p) - 1, len(p) - 1])
            else:
                con.append([i + j * NT - 1, 1 + i + j * NT - 1])  # add the horizontal line into geometry
                sur.append([i + j * NT - 1, 1 + i + j * NT - 1, len(p) - 1, len(p) - 1])
        else:
            con.append([i + j * NT - 1, i + (j + 1) * NT - 1])  # add the vertical line into geometry
            if i == NT:
                con.append([i + j * NT - 1, 1 + i + (j - 1) * NT - 1])  # add the horizontal line into geometry
                sur.append([i + j * NT - 1, 1 + i + (j - 1) * NT - 1, i + (j + 1) * NT - 1, 1 + i + j * NT - 1])
            else:
                con.append([i + j * NT - 1, 1 + i + j * NT - 1])  # add the horizontal line into geometry
                sur.append([i + j * NT - 1, 1 + i + j * NT - 1, i + (j + 1) * NT - 1, 1 + i + (j + 1) * NT - 1])

cwd = os.getcwd()
np.savetxt(cwd + '/lines.txt', con)
np.savetxt(cwd + '/surfaces.txt', sur)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for item in p:
    ax.scatter(item[0], item[1], item[2])
for item in con:
    ax.plot([p[item[0]][0], p[item[1]][0]],
            [p[item[0]][1], p[item[1]][1]],
            [p[item[0]][2], p[item[1]][2]])
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()
