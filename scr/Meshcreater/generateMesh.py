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
    "cylindrical-NoBottom",
    "cylindrical-WithBottom",
    "squared-NoBottom",
    "squared-WithBottom",
]  # add more models if it is ready
if cageinfo['CageShape']['shape'] in cageTypes:
    if cageinfo['Mooring']['mooringType'] in ['None']:
        os.system(str(workPath.salome_path) + " -t " + workPath.mesh_path + "ME_single_cage.py " + "args:" + Dictname)
    else:
        print("cage with mooring system is not finished yet, please wait for a update.")
        exit()
else:
    printmodel()
    exit()
