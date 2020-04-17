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
import numpy as np
from utilityScritp import post_subFunctions as ps
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams['font.weight'] = 'regular'
plt.rcParams['font.size'] = '10'
plt.rcParams["mathtext.default"] = "it"
plt.rcParams["mathtext.fontset"] = "stix"
font = {'family': 'Times New Roman', 'style': 'italic', 'weight': 'regular', 'size': 10}

# >>>>>>>>>>>>>>  read file
file = "../../../FSItest/test1/constant/forceOnNetting.txt"
force = ps.read_force(file)

# >>>>>>>>>>>>>> plotting
fig = plt.figure(figsize=(6.3, 4.2))  # figsize in rinche
plt.plot(force[:, 0], force[:, 1], color='r', label="Fx")
# plt.plot(force[:,0],force[:,2],color='g',label="Fy")
# plt.plot(force[:,0],force[:,3],color='b',label="Fz")
plt.legend()
plt.xlim([0, 10])
plt.ylim([15, 35])
plt.xlabel("Drag Force (N)")
plt.ylabel("Time (s)")

plt.show()
