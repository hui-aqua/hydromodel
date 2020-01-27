"""
/--------------------------------\
|    University of Stavanger     |
|           Hui Cheng            |
\--------------------------------/
Any questions about this code, please email: hui.cheng@uis.no

"""
import os
import sys
import workPath
import numpy as np

cwd=os.getcwd()
print("The working folder is ' "+str(cwd)+ " ' \n")
os.system("python3 " + workPath.mesh_path + "generateMesh.py " + str(sys.argv[1]))
