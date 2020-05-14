"""
----------------------------------------------
--         University of Stavanger          --
--         Hui Cheng (PhD student)          --
--          Lin Li (Medveileder)            --
--      Prof. Muk Chen Ong (Supervisor)     --
----------------------------------------------
Any questions about this code,
please email: hui.cheng@uis.no
"""
import numpy as np
import matplotlib.cm as cm
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gc
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
from utilityScritp import post_subFunctions as ps
import os
import ast

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams['font.weight'] = 'regular'
plt.rcParams['font.size'] = '10'
plt.rcParams["mathtext.default"] = "it"
plt.rcParams["mathtext.fontset"] = "stix"
font = {'family': 'Times New Roman', 'style': 'italic', 'weight': 'regular', 'size': 10}

# >>>>>>>>>>>>>>  read file
file_name = "../../../FSItest/test1_3_1.03/constant/velocity_on_element.txt"
with open(file_name, 'r') as f:
    content = f.read()
    velocity_dict = ast.literal_eval(content)

time_selected = 12.2
U, u_mean = ps.read_velocity_dict(time_selected, velocity_dict)

# >>>>>>>>>>>>> plotting (1) velocity histogram
plt.figure(figsize=(4.3, 3.2))
titles = ['U_mag', 'U_x', 'U_y', 'U_z']
gs = gc.GridSpec(1, 1)
for i in range(1):
    ax = plt.subplot(gs[i])
    plt.title(titles[i] + " at " + str(time_selected) + "s")
    ax.hist(U[i], 20)
    ax.plot([u_mean[i], u_mean[i]], [0, len(U[0]) / 4], linestyle='--', color='r')
    plt.ylabel("Number")
    plt.xlabel("velocity (m/s)")
plt.tight_layout()
plt.show()

# >>>>>>>>>>>>>> plotting (2) special averaged velocity magnitude historical result


time_list = np.array([float(i) for i in velocity_dict["time_record"][1:]])
velocities_list = np.zeros((len(time_list), 4))
for index, t in enumerate(velocity_dict["time_record"][1:]):
    U, u_mean = ps.read_velocity_dict(t, velocity_dict)
    velocities_list[index] = np.array([u_mean])

plt.figure(figsize=(6.3, 4.2))
plt.plot(time_list, velocities_list[:, 0])
plt.xlim(0, 50)
plt.ylim(0.47, 0.51)
plt.xlabel("Time (s)")
plt.ylabel("Velocity (m/s)")
plt.tight_layout()
plt.show()
