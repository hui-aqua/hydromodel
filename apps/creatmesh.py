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

if len(sys.argv) < 2:
    print("\nNo input dictionary file. \n"
          "Usage: aquaMesh + [dictionary name]\n"
          "i.e., aquaMesh cage1\n"
          "The dictionary file follows the Python's syntax.\n ")
    exit()

with open(str(sys.argv[1]), 'r') as f:
    content = f.read()
    cageInfo = ast.literal_eval(content)
floater_num = int(np.array(cageInfo['FloatingCollar']['floaterCenter']).size / 3)

cage_shape_types = [
    "cylindrical-NoBottom",
    "cylindrical-WithBottom",
    "squared-NoBottom",
    "squared-WithBottom",
]  # add more models if it is ready

def print_model():
    print("The cage type '" + cageInfo['CageShape']['CageType'] + "' are not included in this version.\n")
    print("Currently, the available numerical models are:")
    for model in cage_shape_types:
        print(str(cage_shape_types.index(model)) + " " + model)


if cageInfo['CageShape']['shape'] not in cage_shape_types:
    print_model()
    exit()
else:
    if cageInfo['Mooring']['mooringType'] not in ['None']:
        os.system(
            str(workPath.salome_path) + " -t " + workPath.mesh_path + "ME_multi_moored_cages.py " + "args:" + str(
                sys.argv[1]))
    else:
        if floater_num == 1:  # Single cage
            os.system(
                str(workPath.salome_path) + " -t " + workPath.mesh_path + "ME_single_cage.py " + "args:" + str(
                    sys.argv[1]))
        else:
            os.system(
                str(workPath.salome_path) + " -t " + workPath.mesh_path + "ME_multi_cages.py " + "args:" + str(
                    sys.argv[1]))
