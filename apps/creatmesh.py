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

meshLib = str(cageInfo['MeshLib'])
os.system(
    str(workPath.salome_path) + " -t " + workPath.mesh_path + "ME_" + meshLib + ".py " + "args:" + str(sys.argv[1]))
