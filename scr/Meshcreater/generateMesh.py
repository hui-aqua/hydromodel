"""
/--------------------------------\
|    University of Stavanger     |
|           Hui Cheng            |
\--------------------------------/
Any questions about this code, please email: hui.cheng@uis.no

Fish cage is along the Z- direction
Z=0 is the free surface
Z<0 is the water zone
Z>0 is the air zone

Run with a arguement [casename]
"""
import sys
import os
import workPath
import numpy as np
from numpy import pi

cwd = os.getcwd()
Dictname = str(sys.argv[1])
with open(Dictname, 'r') as f:
    content = f.read()
    cageinfo = eval(content)


def printmodel():
    print("The cage type '" + cageinfo['CageShape']['CageType'] + "' are not included in this version.\n")
    print("Currently, the available numerical models are:")
    for model in cageTypes:
        print(str(cageTypes.index(model)) + " " + model)


cageTypes = [
    "cylindricalNoBottom",
    "cylindricalWithBottom",
    "squaredNoBottom",
    "squaredWithBottom",
    "cylindricalWithBottomWithMooring",
    "trawlnet",
    'threecages'
]  # add more models if it is ready
if cageinfo['CageShape']['shape'] in cageTypes:
    os.system(str(workPath.salome_path) + " -t " + workPath.mesh_path + "ME_" + cageinfo['CageShape'][
        'shape'] + ".py " + "args:" + Dictname)
else:
    printmodel()
    exit()
