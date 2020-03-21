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
import workPath
import numpy as np
import socket
import getpass
import scr.inputfilecreator.inputModule as im
# import inputModule as im
cwd = os.getcwd()
argument = sys.argv

with open(str(sys.argv[1]), 'r') as f:
    content = f.read()
    cageInfo = eval(content)

sys.path.append(cwd)
import meshinfomation

switcher = cageInfo['Solver']['coupling']
hydroModel = str(cageInfo['Net']['HydroModel'])

Fbuoy = meshInfo['horizontalElementLength'] * meshInfo['verticalElementLength'] * cageInfo['Net']['Sn'] / \
        cageInfo['Net']['twineDiameter'] * 0.25 * np.pi * pow(cageInfo['Net']['twineDiameter'], 2) * 9.81 * float(
    cageInfo['Environment']['fluidDensity'])
# Buoyancy force to assign on each nodes
dwh = meshInfo['horizontalElementLength'] * meshInfo['verticalElementLength'] * cageInfo['Net']['Sn'] / (
        meshInfo['horizontalElementLength'] + meshInfo['verticalElementLength'])
# hydrodynamic diameter to calculate the hydrodynamic coefficient.
lam1 = meshInfo['horizontalElementLength'] / cageInfo['Net']['meshLength']
lam2 = meshInfo['verticalElementLength'] / cageInfo['Net']['meshLength']
dws = np.sqrt(2 * lam1 * lam2 / (lam1 + lam2)) * cageInfo['Net']['twineDiameter']
twineSection = 0.25 * np.pi * pow(dws, 2)
dt = cageInfo['Solver']['timeStep']  # time step

