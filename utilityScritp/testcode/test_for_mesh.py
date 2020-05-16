"""
-------------------------------------------\n
-         University of Stavanger          \n
-         Hui Cheng (PhD student)          \n
-          Lin Li (Medveileder)            \n
-      Prof. Muk Chen Ong (Supervisor)     \n
-------------------------------------------\n
Any questions about this code,
please email: hui.cheng@uis.no \n
"""
import sys
import os
import numpy as np
from numpy import pi
import ast
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import matplotlib.pyplot as plt

point = []  # points on netting
con = []  # lines on netting
sur = []  # surface on netting
mcon = []  # lines on mooring
wcon = []  # lines on weight lines
cwd = os.getcwd()

NT = 32  # Number of the nodes in circumference
NN = 5
BN = 5
floater_center = [0, 0, 0]
cage_diameter = 12
cage_height = 6
cage_cone_height = 7
all_point_list = []
# generate the point coordinates matrix for cylindrical cage
for j in range(0, NN + 1):
    for i in range(0, NT):
        point.append(
            [floater_center[0] + cage_diameter / 2 * np.cos(i * 2 * pi / float(NT)),
             floater_center[1] + cage_diameter / 2 * np.sin(i * 2 * pi / float(NT)),
             floater_center[2] - j * cage_height / float(NN)])

for j in range(1, BN):
    for i in range(0, NT):
        point.append(
            [floater_center[0] + cage_diameter / 2 * ((BN - j) / BN) * np.cos(i * 2 * pi / float(NT)),
             floater_center[1] + cage_diameter / 2 * ((BN - j) / BN) * np.sin(i * 2 * pi / float(NT)),
             floater_center[2] - cage_height - j * (cage_cone_height - cage_height) / float(BN)])

point.append([floater_center[0], floater_center[1], -cage_cone_height])

# for j in range(0, NN + 1):
#     point_in_circum=[]
#     for i in range(0, NT):
#         point_in_circum.append(
#             [floater_center[0] + cage_diameter / 2 * np.cos(i * 2 * pi / float(NT)),
#              floater_center[1] + cage_diameter / 2 * np.sin(i * 2 * pi / float(NT)),
#              floater_center[2] - j * cage_height / float(NN)])
#     all_point_list.append(point_in_circum)


point_numpy = np.array(point)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
p = ax.scatter(point_numpy[:, 0],
               point_numpy[:, 1],
               point_numpy[:, 2])
