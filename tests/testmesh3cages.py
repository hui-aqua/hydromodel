import numpy as np
from numpy import pi

D = 1.75  # [m]  fish cage diameter

H = 1.5  # [m]  fish cage height
NT = 24  # it can use int(pi*D/L)   # Number of the nodes in circumference
NN = 7  # it can use int(H/L)      # number of section in the height, thus, the nodes should be NN+1
p = []
con = []
sur = []
FloatingCenter = [[0.0, 0.0, 0.0], [2 * 1.75, 0.0, 0.0], [4 * 1.75, 0.0, 0.0]]
Num_nodesInOneCage = NT * (NN + 1)

# the below is the commond in the Mesh, Salome.
# the mesh creater script
for cageI in range(len(FloatingCenter)):
    print("Creating cage  " + str(cageI))
    for j in range(0, NN + 1):
        for i in range(0, NT):
            p.append([FloatingCenter[cageI][0] + D / 2 * np.cos(i * 2 * pi / float(NT)),
                      FloatingCenter[cageI][1] + D / 2 * np.sin(i * 2 * pi / float(NT)),
                      FloatingCenter[cageI][2] - j * H / float(NN)])

for cageI in range(len(FloatingCenter)):
    for i in range(1, NT + 1):
        for j in range(0, NN + 1):
            if j == NN:
                if i == NT:
                    con.append([i + j * NT + Num_nodesInOneCage * cageI - 1, 1 + i + (
                                j - 1) * NT + Num_nodesInOneCage * cageI - 1])  # add the horizontal line into con
                else:
                    con.append([i + j * NT - 1 + Num_nodesInOneCage * cageI,
                                1 + i + j * NT - 1 + Num_nodesInOneCage * cageI])  # add the horizontal line into con
            else:
                con.append([i + j * NT - 1 + Num_nodesInOneCage * cageI,
                            i + (j + 1) * NT - 1 + Num_nodesInOneCage * cageI])  # add the vertical line into con
                if i == NT:
                    con.append([i + j * NT - 1 + Num_nodesInOneCage * cageI,
                                1 + i + (
                                            j - 1) * NT - 1 + Num_nodesInOneCage * cageI])  # add the horizontal line into con
                    sur.append([i + j * NT - 1 + Num_nodesInOneCage * cageI,
                                1 + i + (j - 1) * NT - 1 + Num_nodesInOneCage * cageI,
                                i + (j + 1) * NT - 1 + Num_nodesInOneCage * cageI,
                                1 + i + j * NT - 1 + Num_nodesInOneCage * cageI])
                # add the horizontal surface into sur
                else:
                    con.append([i + j * NT - 1 + Num_nodesInOneCage * cageI,
                                1 + i + j * NT - 1 + Num_nodesInOneCage * cageI])  # add the horizontal line into con
                    sur.append([i + j * NT - 1 + Num_nodesInOneCage * cageI,
                                1 + i + j * NT - 1 + Num_nodesInOneCage * cageI,
                                i + (j + 1) * NT - 1 + Num_nodesInOneCage * cageI,
                                1 + i + (j + 1) * NT - 1 + Num_nodesInOneCage * cageI])
                # add the horizontal surface into sur
numberOfNodes = len(p)
numberOfLines = len(con)
numberOfSurfaces = len(sur)

from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

import matplotlib
import matplotlib.pyplot as plt

nodesx = []
nodesy = []
nodesz = []
for nodI in p:
    nodesx.append(nodI[0])
    nodesy.append(nodI[1])
    nodesz.append(nodI[2])

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(nodesx, nodesy, nodesz)
# # >>>>>>>plot line
# for line in con:
#     xs=[nodesx[line[0]],nodesx[line[1]]]
#     ys=[nodesy[line[0]],nodesy[line[1]]]
#     zs=[nodesz[line[0]],nodesz[line[1]]]
#     ax.plot(xs,ys,zs)

i = 0
for surf in sur:
    i += 1
    if i < 10000:
        xs = [nodesx[surf[0]], nodesx[surf[1]], nodesx[surf[2]], nodesx[surf[3]], nodesx[surf[1]], nodesx[surf[2]],
              nodesx[surf[0]], nodesx[surf[3]]]
        ys = [nodesy[surf[0]], nodesy[surf[1]], nodesy[surf[2]], nodesy[surf[3]], nodesy[surf[1]], nodesy[surf[2]],
              nodesy[surf[0]], nodesy[surf[3]]]
        zs = [nodesz[surf[0]], nodesz[surf[1]], nodesz[surf[2]], nodesz[surf[3]], nodesz[surf[1]], nodesz[surf[2]],
              nodesz[surf[0]], nodesz[surf[3]]]
        ax.plot(xs, ys, zs)
