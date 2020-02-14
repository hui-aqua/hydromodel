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
import numpy as np
import sys
import os
import workPath
import ast

cwd = os.getcwd()
with open(str(sys.argv[1]), 'r') as f:
    content = f.read()
    cageInfo = ast.literal_eval(content)

cageTypes = [
    "cylindrical-NoBottom",
    "cylindrical-WithBottom",
    "squared-NoBottom",
    "squared-WithBottom",
]  # add more models if it is ready


def print_model():
    print("The cage type '" + cageInfo['CageShape']['CageType'] + "' are not included in this version.\n")
    print("Currently, the available numerical models are:")
    for model in cageTypes:
        print(str(cageTypes.index(model)) + " " + model)


floater_num = np.array(cageInfo['FloatingCollar']['floaterCenter']).size

if floater_num == 3:  # Single cage
    if cageInfo['CageShape']['shape'] in cageTypes:
        if cageInfo['Mooring']['mooringType'] in ['None']:
            os.system(
                str(workPath.salome_path) + " -t " + workPath.mesh_path + "ME_single_cage.py " + "args:" + str(
                    sys.argv[1]))
        else:
            print("cage with mooring system is not finished yet, please wait for a update.")
            exit()
    else:
        print_model()
        exit()
elif floater_num % 3 == 0 and floater_num > 3:  # multi_fixed cage
    os.system(
        str(workPath.salome_path) + " -t " + workPath.mesh_path + "ME_multi_cages.py " + "args:" + str(sys.argv[1]))
