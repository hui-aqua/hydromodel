import os
import sys
import workPath

# os.system("clear")
# if not os.path.isfile('cageDict'):
#     print("\n Please make sure cageDict is located in the working path.\n")
#     exit()

os.system("python3 " + workPath.mesh_path + "generateMesh.py " + str(sys.argv[1]))
