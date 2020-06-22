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
import os
import sys
import random as rd
import numpy as np
import socket
import getpass
import inputModule as im
# from scr.inputfilecreator import inputModule as im
import ast

cwd = os.getcwd()
argument = sys.argv

cwd = os.getcwd()
suffix = rd.randint(1, 10000)
hostname = socket.gethostname()
username = getpass.getuser()
argument = sys.argv

with open(str(sys.argv[1]), 'r') as f:
    content = f.read()
    cageInfo = ast.literal_eval(content)

sys.path.append(cwd)
import meshInformation

dw0 = float(cageInfo['Net']['twineDiameter'])
coupling_switcher = cageInfo['Solver']['coupling']  #
hydrodynamic_model = str(cageInfo['Boundary']['hydroModel'])
hydrodynamic_model_rope = "M4"
wake_model = str(cageInfo['Boundary']['wakeModel'])
time_thread = cageInfo['Boundary']['currentForceIncreasing']
cage_array = str(cageInfo['Mooring']['cageArray'])
number_of_cage_X = int(cage_array.split("-")[0])
number_of_cage_Y = int(cage_array.split("-")[1])

Fbuoy = number_of_cage_Y * number_of_cage_X * (
        np.pi * cageInfo['CageShape']['cageDiameter'] * cageInfo['CageShape']['cageHeight'] + 0.5 * np.pi *
        cageInfo['CageShape']['cageDiameter'] * np.sqrt(pow(cageInfo['CageShape']['cageDiameter'] / 2, 2) + pow(
    cageInfo['CageShape']['cageConeHeight'] - cageInfo['CageShape']['cageHeight'], 2))) * cageInfo['Net'][
            'Sn'] * dw0 * 0.25 * np.pi * 9.81 * float(cageInfo['Environment']['fluidDensity'])
print("Fbuoy is " + str(Fbuoy))
Fb_node = Fbuoy / float(meshInformation.meshinfo['numberOfNodes_netting'])
print("For each node on netting, the buoy force is " + str(Fb_node))

lam1 = float(meshInformation.meshinfo['horizontalElementLength'] / cageInfo['Net']['meshLength'])
lam2 = float(meshInformation.meshinfo['verticalElementLength'] / cageInfo['Net']['meshLength'])

dwh = dw0 * 2 * lam1 * lam2 / (lam1 + lam2)

# hydrodynamic diameter to calculate the hydrodynamic coefficient.
dws = dw0 * np.sqrt(2 * lam1 * lam2 / (lam1 + lam2))
dwe = dws

print("dw0, dwh,dws,dwe are " + str(dw0) + ", " + str(dwh) + ", " + str(dws) + ", " + str(dwe) + ",")
twineSection = 0.25 * np.pi * pow(dws, 2)

dt = cageInfo['Solver']['timeStep']  # time step
velocities = cageInfo['Environment']['current']

# input file 1
handle1 = open(cwd + '/ASTER1.py', 'w')
im.head(handle1, cwd)
im.define_model_fishFarm(handle1, twineSection, Fb_node)
im.define_time_scheme(handle1, cageInfo['Solver']['timeStep'], cageInfo['Solver']['timeLength'], len(velocities))
im.set_hydrodynamic_model_fishFarm(handle1, velocities, cageInfo['Environment']["fluidDensity"], cageInfo['Net']['Sn'],
                                   dwh, dw0)
handle1.close()

# input file 2
handle2 = open(cwd + '/ASTER2.py', 'w')
im.set_dyna_solver_fishFarm(handle2, cageInfo['Solver']['alpha'], time_thread, coupling_switcher)

handle2.close()

# input file 3
handle3 = open(cwd + '/ASTERRUN.export', 'w')
im.set_export(handle3, suffix, hostname, username, cwd, cageInfo['Solver']['version'],
              meshInformation.meshinfo['meshName'])

handle3.close()

print("\nALL finished! You can check the input file manually and run 'aquaSim' to start the simulation\n")
