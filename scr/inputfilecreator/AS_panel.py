"""
----------------------------------------------
--         University of Stavanger          --
--         Hui Cheng (PhD student)          --
--          Lin Li (Medveileder)            --
--     Prof. Muk Chen Ong (Supervisor)      --
----------------------------------------------
Any questions about this code,
please email: hui.cheng@uis.no

"""
import os
import sys
import random as rd
import numpy as np
import socket
import getpass
import ast
# from scr.inputfilecreator import inputModule as im

import inputModule as im

cwd = os.getcwd()
suffix = rd.randint(1, 10000)
hostname = socket.gethostname()
username = getpass.getuser()
argument = sys.argv

with open(str(sys.argv[1]), 'r') as f:
    content = f.read()
    netPanelInfo = ast.literal_eval(content)

sys.path.append(cwd)
import meshinfomation

dw0 = netPanelInfo['Net']['twineDiameter']
coupling_switcher = netPanelInfo['Solver']['coupling']  #
hydrodynamic_model = str(netPanelInfo['Net']['hydroModel'])
wake_model = str(netPanelInfo['Net']['wakeModel'])

Fbuoy = netPanelInfo['Net']['netHeight'] * netPanelInfo['Net']['netWidth'] * \
        netPanelInfo['Net']['Sn'] * dw0 * 0.25 * np.pi * 9.81 * float(
    netPanelInfo['Environment']['fluidDensity'])
print("Fbuoy is " + str(Fbuoy))
# Buoyancy force to assign on each nodes

lam1 = meshinfomation.meshinfo['horizontalElementLength'] / netPanelInfo['Net']['meshLength']
lam2 = meshinfomation.meshinfo['verticalElementLength'] / netPanelInfo['Net']['meshLength']

dwh = dw0 * 2 * lam1 * lam2 / (lam1 + lam2)

# hydrodynamic diameter to calculate the hydrodynamic coefficient.
dws = dw0 * np.sqrt(2 * lam1 * lam2 / (lam1 + lam2))
dwe = dws
twineSection = 0.25 * np.pi * pow(dws, 2)
dt = netPanelInfo['Solver']['timeStep']  # time step
velocities = netPanelInfo['Environment']['current']
print("dw0, dwh,dws,dwe are "+str(dw0)+"[m], "+str(dwh)+"[m], "+str(dws)+"[m], "+str(dwe)+"[m].")
# input file 1
handle1 = open(cwd + '/ASTER1.py', 'w')
im.head(handle1, cwd)
im.define_model(handle1, netPanelInfo['Weight']['weightType'])
im.define_element(handle1, netPanelInfo['Weight']['weightType'], twineSection,
                  netPanelInfo['Weight']['bottomBarRadius'])
im.define_material(handle1, netPanelInfo['Weight']['weightType'], netPanelInfo['Net']["netYoungmodule"],
                   netPanelInfo['Net']["netRho"], netPanelInfo['Weight']["bottomBarYoungModule"],
                   netPanelInfo['Weight']["bottomBarRho"])
im.assign_material(handle1, netPanelInfo['Weight']['weightType'])

im.assign_bc_gravity(handle1, 'gF', 9.81, 'twines')
im.assign_bc_force_on_nodes(handle1, 'buoyF', 'allnodes',
                            [0, 0, Fbuoy / float(meshinfomation.meshinfo['numberOfNodes'])])

if netPanelInfo['Weight']['weightType'] in ['sinkers']:
    im.assign_bc_fixed(handle1, 'fixed', 'topnodes')
    im.assign_bc_force_on_nodes(handle1, 'sinkF', 'sinkers', [0, 0, netPanelInfo['Weight']["sinkerWeight"]])
elif netPanelInfo['Weight']['weightType'] in ['allFixed']:
    im.assign_bc_fixed(handle1, 'fixed', 'allnodes')
else:
    im.assign_bc_fixed(handle1, 'fixed', 'topnodes')

im.define_time_scheme(handle1, netPanelInfo['Solver']['timeStep'], netPanelInfo['Solver']['timeLength'],
                      len(velocities))
im.set_hydrodynamic_model(handle1, hydrodynamic_model, wake_model, netPanelInfo['Net']['Sn'], dwh, dw0,
                          netPanelInfo['Environment']['current'],netPanelInfo['Environment']["fluidDensity"])
im.reaction_force(handle1, 'topnodes')
handle1.close()

# input file 2
handle2 = open(cwd + '/ASTER2.py', 'w')
im.apply_boundary(handle2, ['gF', 'fixed', 'buoyF'])
im.set_dyna_solver(handle2, netPanelInfo['Weight']['weightType'], netPanelInfo['Solver']['MaximumIteration'],
                   netPanelInfo['Solver']['Residuals'], netPanelInfo['Solver']['method'],
                   netPanelInfo['Solver']['alpha'])
im.set_coupling(handle2, coupling_switcher)
im.set_save_midresults(handle2, netPanelInfo['Solver']['saveMid_result'])
handle2.close()

# input file 3
handle3 = open(cwd + '/ASTERRUN.export', 'w')
im.set_export(handle3, suffix, hostname, username, cwd, netPanelInfo['Solver']['version'], meshinfomation.meshinfo['meshName'])

handle3.close()

print("\nALL finished! You can check the input file manually and run 'aquaSim' to start the simulation\n")
