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
# from scr.inputfilecreator import inputModule as im

import inputModule as im

cwd = os.getcwd()
suffix = rd.randint(1, 10000)
hostname=socket.gethostname()
username=getpass.getuser()
argument = sys.argv

with open(str(sys.argv[1]), 'r') as f:
    content = f.read()
    cageInfo = eval(content)

sys.path.append(cwd)
import meshinfomation

dw0 = cageInfo['Net']['twineDiameter']
coupling_switcher = cageInfo['Solver']['coupling']  #
hydroModel = str(cageInfo['Net']['HydroModel'])

Fbuoy = meshinfomation.meshinfo['horizontalElementLength'] * meshinfomation.meshinfo['verticalElementLength'] * \
        cageInfo['Net']['Sn'] / \
        dw0 * 0.25 * np.pi * pow(dw0, 2) * 9.81 * float(
    cageInfo['Environment']['fluidDensity'])
# Buoyancy force to assign on each nodes
lam1 = meshinfomation.meshinfo['horizontalElementLength'] / cageInfo['Net']['meshLength']
lam2 = meshinfomation.meshinfo['verticalElementLength'] / cageInfo['Net']['meshLength']

dwh = dw0 * 2 * lam1 * lam2 / (lam1 + lam2)

# hydrodynamic diameter to calculate the hydrodynamic coefficient.
dws = dw0 * np.sqrt(2 * lam1 * lam2 / (lam1 + lam2))
dwe = dws
twineSection = 0.25 * np.pi * pow(dws, 2)
dt = cageInfo['Solver']['timeStep']  # time step
velocities = cageInfo['Environment']['current']

# input file 1
handle1 = open(cwd + '/ASTER1.comm', 'w')
im.head(handle1, cwd)
im.define_model(handle1, cageInfo['Weight']['weightType'])
im.define_element(handle1, cageInfo['Weight']['weightType'], twineSection, cageInfo['Weight']['bottomBarRadius'])
im.define_material(handle1, cageInfo['Weight']['weightType'], cageInfo['Net']["netYoungmodule"],
                   cageInfo['Net']["netRho"], cageInfo['Weight']["bottomBarYoungModule"],
                   cageInfo['Weight']["bottomBarRho"])
im.assign_material(handle1, cageInfo['Weight']['weightType'])
im.assign_bc_gravity(handle1, 'gF', 9.81, 'twines')
im.assign_bc_fixed(handle1, 'fixed', 'topnodes')
im.assign_bc_force_on_nodes(handle1, 'buoyF', 'allnodes', [0, 0, Fbuoy])
im.assign_bc_force_on_nodes(handle1, 'sinkF', 'sinkers', [0, 0, cageInfo['Weight']["sinkerWeight"]])
im.define_time_scheme(handle1, cageInfo['Solver']['timeStep'], cageInfo['Solver']['timeLength'], len(velocities))
im.reaction_force(handle1, 'topnodes')
handle1.close()

# input file 2
handle2 = open(cwd + '/ASTER2.comm', 'w')
im.apply_boundary(handle2, ['gF', 'fixed', 'buoyF', 'sinkF'])
im.set_dyna_solver(handle2, cageInfo['Weight']['weightType'], cageInfo['Solver']['MaximumIteration'],
                   cageInfo['Solver']['Residuals'], cageInfo['Solver']['method'], cageInfo['Solver']['alpha'])
im.set_hydrodynamic_model(handle2, hydroModel, cageInfo['Net']['Sn'], dwh, dw0,cageInfo['Environment']['current'])
im.set_coupling(handle2,coupling_switcher)
im.set_save_midresults(handle2,cageInfo['Solver']['saveMid_result'])
handle2.close()

# input file 3
handle3 = open(cwd + '/ASTERRUN.export', 'w')
im.set_export(handle3,suffix,hostname,username,cwd,'stable',meshinfomation.meshinfo['meshName'])

handle3.close()