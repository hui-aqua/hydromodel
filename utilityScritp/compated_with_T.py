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
import ast
from utilityScritp import post_subFunctions as ps
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams['font.weight'] = 'regular'
plt.rcParams['font.size'] = '10'
plt.rcParams["mathtext.default"] = "it"
plt.rcParams["mathtext.fontset"] = "stix"
font = {'family': 'Times New Roman', 'style': 'italic', 'weight': 'regular', 'size': 10}

# >>>>>>>>>>>>>>  read file
files = ["../../../FSItest/test1/constant/forceOnNetting.txt",
         "../../../FSItest/test1_3/constant/forceOnNetting.txt",
         "../../../FSItest/test1_5/constant/forceOnNetting.txt",
         "../../../FSItest/test1_7/constant/forceOnNetting.txt"]

labels = ['T1', "T3", "T5", "T7"]

# >>>>>>>>>>>>>> plotting 1 force
fig = plt.figure(figsize=(6.3, 4.2))  # figsize in rinche
for file in files:
    force = ps.read_force(file)
    plt.plot(force[:, 0], force[:, 1], label=labels[files.index(file)])
plt.plot([0, 50], [32.25, 32.25], '--k', label="Paturrsson et al. 2010")
plt.legend()
plt.xlim(0, 30)
plt.ylim([15, 35])
plt.ylabel("Drag Force (N)")
plt.xlabel("Time (s)")
plt.show()

# >>>>>>>>>>>>>>  read file
files = ["../../../FSItest/test1_3/constant/forceOnNetting.txt",
         "../../../FSItest/test1_3_1.05/constant/forceOnNetting.txt",
         "../../../FSItest/test1_3_1.1/constant/forceOnNetting.txt",
         "../../../FSItest/test1_3_1.2/constant/forceOnNetting.txt",
         # "../../../FSItest/test1_3_1.3/constant/forceOnNetting.txt"
         ]

labels = ['T3_1', "T3_1.05", "T3_1.1", "T3_1.2", "T3_1.3"]

# >>>>>>>>>>>>>> plotting 2 force
fig = plt.figure(figsize=(6.3, 4.2))  # figsize in rinche
for file in files:
    force = ps.read_force(file)
    plt.plot(force[:, 0], force[:, 1], label=labels[files.index(file)])
plt.plot([0, 50], [32.25, 32.25], '--k', label="Paturrsson et al. 2010")
plt.legend()
plt.xlim(0, 30)
plt.ylim([15, 45])
plt.ylabel("Drag Force (N)")
plt.xlabel("Time (s)")

plt.show()

# >>>>>>>>>>>>>>  read file
files = ["../../../FSItest/test1/constant/velocity_on_element.txt",
         "../../../FSItest/test1_3/constant/velocity_on_element.txt",
         "../../../FSItest/test1_5/constant/velocity_on_element.txt",
         "../../../FSItest/test1_7/constant/velocity_on_element.txt"]
labels = ['T1', "T3", "T5", "T7"]
# >>>>>>>>>>>>>> plotting 3 velocity

fig = plt.figure(figsize=(6.3, 4.2))  # figsize in rinche

for file in files:
    with open(file, 'r') as f:
        content = f.read()
        velocity_dict = ast.literal_eval(content)

    time_list = np.array([float(i) for i in velocity_dict["time_record"][1:]])
    velocities_list = np.zeros((len(time_list), 4))
    for index, t in enumerate(velocity_dict["time_record"][1:]):
        U, u_mean = ps.read_velocity_dict(t, velocity_dict)
        velocities_list[index] = np.array([u_mean])
    plt.plot(time_list, velocities_list[:, 0], label=labels[files.index(file)])
plt.xlim(0, 30)
plt.ylim(0.46, 0.51)
plt.legend()
plt.xlabel("Time (s)")
plt.ylabel("Velocity (m/s)")
plt.tight_layout()
plt.show()

# >>>>>>>>>>>>>>  read file
files = ["../../../FSItest/test1_3/constant/velocity_on_element.txt",
         "../../../FSItest/test1_3_1.05/constant/velocity_on_element.txt",
         "../../../FSItest/test1_3_1.1/constant/velocity_on_element.txt",
         "../../../FSItest/test1_3_1.2/constant/velocity_on_element.txt",
         # "../../../FSItest/test1_3_1.3/constant/velocity_on_element.txt"
         ]

labels = ['T1_3_1', "T3_1.05", "T3_1.1", "T3_1.2", "T3_1.3"]

# >>>>>>>>>>>>>> plotting 4 velocity

fig = plt.figure(figsize=(6.3, 4.2))  # figsize in rinche

for file in files:
    with open(file, 'r') as f:
        content = f.read()
        velocity_dict = ast.literal_eval(content)

    time_list = np.array([float(i) for i in velocity_dict["time_record"][1:]])
    velocities_list = np.zeros((len(time_list), 4))
    for index, t in enumerate(velocity_dict["time_record"][1:]):
        U, u_mean = ps.read_velocity_dict(t, velocity_dict)
        velocities_list[index] = np.array([u_mean])
    plt.plot(time_list, velocities_list[:, 0], label=labels[files.index(file)])
plt.plot([0, 50], [0.5, 0.5])
plt.xlim(0, 30)
plt.ylim(0.45, 0.55)
plt.legend()
plt.xlabel("Time (s)")
plt.ylabel("Velocity (m/s)")
plt.tight_layout()
plt.show()
