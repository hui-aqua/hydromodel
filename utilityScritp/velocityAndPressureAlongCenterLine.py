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
import matplotlib.pyplot as plt
from utilityScritp import post_subFunctions as ps

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams['font.weight'] = 'regular'
plt.rcParams['font.size'] = '10'
plt.rcParams["mathtext.default"] = "it"
plt.rcParams["mathtext.fontset"] = "stix"
font = {'family': 'Times New Roman', 'style': 'italic', 'weight': 'regular', 'size': 10}

time_select = 50
file = "../../../FSItest/test1_3_1.05/postProcessing/singleGraph/" + str(time_select) + "/line_p.xy"
pressure = ps.read_pressureXY(file)

file = "../../../FSItest/test1_3_1.05/postProcessing/singleGraph/" + str(time_select) + "/line_U.xy"
velocity = ps.read_velocityXY(file)

# fig = plt.figure(figsize=(6.3, 4.2))  # figsize in rinche
fig, ax1 = plt.subplots(figsize=(6.3, 3.2))

ax1.plot(pressure[:, 0], pressure[:, 1] - pressure[0, 1], color='r')
ax1.plot([-3, 5], [0, 0], color='k', linestyle='--', linewidth='0.5')
ax1.plot([-0.06, -0.06], [-0.05, 0.05], color='k', linestyle='--', linewidth='0.7')
ax1.plot([0.075, 0.075], [-0.05, 0.05], color='k', linestyle='--', linewidth='0.7')

ax1.set_xlabel('X (m)')
ax1.set_ylabel('Pressure (Pa)', color='r')
ax1.tick_params(axis='y', labelcolor='r')
ax1.set_ylim(-0.05, 0.05)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

ax2.set_ylabel('Velocity (m/s)', color='b')  # we already handled the x-label with ax1
ax2.plot(velocity[:, 0], velocity[:, 4], color='b')
ax2.tick_params(axis='y', labelcolor='b')

plt.xlim(-3, 4.5)
fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.show()
plt.savefig("../../../FSItest/test1_3_1.05/velocityPressureAlongX.png", dpi=900)

fig = plt.figure(figsize=(6.3, 3.2))  # figsize in rinche
cd = np.linspace(0.01, 0.5, 20)
y1 = cd / (2 * (np.sqrt(1 + cd) - 1))
y2 = np.sqrt(2 / (2 - cd))
plt.plot(cd, y1, label="Matin")
plt.plot(cd, y2, label="Cheng")
plt.xlim(0, 0.5)
plt.legend()
plt.savefig("../../../FSItest/test1_3_1.05/velocityPressureAlongX2.png", dpi=900)

cd = np.array([0.258, 0.243, 0.210, 0.157, 0.106, 0.077])
cl = np.array([0, 0.037, 0.064, 0.075, 0.069, 0.035])
r = np.sqrt(1 - (cd + cl))
