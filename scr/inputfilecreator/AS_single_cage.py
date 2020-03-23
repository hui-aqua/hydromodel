"""
----------------------------------
--   University of Stavanger    --
--           Hui Cheng          --
----------------------------------
Any questions about this code, please email: hui.cheng@uis.no

"""
import os
import sys
import random as rd
import numpy as np
import socket
import getpass
import inputModule as im
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
import meshinfomation

dw0 = float(cageInfo['Net']['twineDiameter'])
coupling_switcher = cageInfo['Solver']['coupling']  #
hydrodynamic_model = str(cageInfo['Net']['hydroModel'])
wake_model = str(cageInfo['Net']['wakeModel'])

Fbuoy = np.pi * cageInfo['CageShape']['cageDiameter'] * cageInfo['CageShape']['cageHeight'] * \
        cageInfo['Net']['Sn'] * dw0 * 0.25 * np.pi * 9.81 * float(cageInfo['Environment']['fluidDensity'])
print("Fbuoy is " + str(Fbuoy))
# Buoyancy force to assign on each nodes
lam1 = float(meshinfomation.meshinfo['horizontalElementLength'] / cageInfo['Net']['meshLength'])
lam2 = float(meshinfomation.meshinfo['verticalElementLength'] / cageInfo['Net']['meshLength'])

dwh = dw0 * 2 * lam1 * lam2 / (lam1 + lam2)

# hydrodynamic diameter to calculate the hydrodynamic coefficient.
dws = dw0 * np.sqrt(2 * lam1 * lam2 / (lam1 + lam2))
dwe = dws
print("dw0, dwh,dws,dwe are "+str(dw0)+", "+str(dwh)+", "+str(dws)+", "+str(dwe)+",")
twineSection = 0.25 * np.pi * pow(dws, 2)
dt = cageInfo['Solver']['timeStep']  # time step
velocities = cageInfo['Environment']['current']

# input file 1
handle1 = open(cwd + '/ASTER1.py', 'w')
im.head(handle1, cwd)
im.define_model(handle1, cageInfo['Weight']['weightType'])
im.define_element(handle1, cageInfo['Weight']['weightType'], twineSection, cageInfo['Weight']['bottomRingRadius'])
im.define_material(handle1, cageInfo['Weight']['weightType'], cageInfo['Net']["netYoungmodule"],
                   cageInfo['Net']["netRho"], cageInfo['Weight']["bottomRingYoungModule"],
                   cageInfo['Weight']["bottomRingRho"])
im.assign_material(handle1, cageInfo['Weight']['weightType'])

im.assign_bc_gravity(handle1, 'gF', 9.81, 'twines')
im.assign_bc_force_on_nodes(handle1, 'buoyF', 'allnodes',
                            [0, 0, Fbuoy / float(meshinfomation.meshinfo['numberOfNodes'])])

if cageInfo['Weight']['weightType'] in ['sinkers']:
    im.assign_bc_fixed(handle1, 'fixed', 'topnodes')
    im.assign_bc_force_on_nodes(handle1, 'sinkF', 'sinkers', [0, 0, -cageInfo['Weight']["sinkerWeight"]])
elif cageInfo['Weight']['weightType'] in ['allFixed']:
    im.assign_bc_fixed(handle1, 'fixed', 'allnodes')
else:
    im.assign_bc_fixed(handle1, 'fixed', 'topnodes')

im.define_time_scheme(handle1, cageInfo['Solver']['timeStep'], cageInfo['Solver']['timeLength'], len(velocities))
im.set_hydrodynamic_model(handle1, hydrodynamic_model, wake_model, cageInfo['Net']['Sn'], dwh, dw0,
                          cageInfo['Environment']['current'])
im.reaction_force(handle1, 'topnodes')
handle1.close()

# input file 2
handle2 = open(cwd + '/ASTER2.py', 'w')
if cageInfo['Weight']['weightType'] in ['sinkers']:
    im.apply_boundary(handle2, ['gF', 'fixed', 'buoyF', 'sinkF'])
else:
    im.apply_boundary(handle2, ['gF', 'fixed', 'buoyF'])
im.set_dyna_solver(handle2, cageInfo['Weight']['weightType'], cageInfo['Solver']['MaximumIteration'],
                   cageInfo['Solver']['Residuals'], cageInfo['Solver']['method'], cageInfo['Solver']['alpha'])
im.set_coupling(handle2, coupling_switcher)
im.set_save_midresults(handle2, cageInfo['Solver']['saveMid_result'])
handle2.close()

# input file 3
handle3 = open(cwd + '/ASTERRUN.export', 'w')
im.set_export(handle3, suffix, hostname, username, cwd, 'stable', meshinfomation.meshinfo['meshName'])

handle3.close()

print("\nALL finished! You can check the input file manually and run 'aquaSim' to start the simulation\n")
