import os
import workPath
os.system("clear")
if not os.path.isfile('cageDict'):
    print("\n Please make sure cageDict is located in the working path.\n")
    exit()

os.system("python3 " + workPath.scr_path + "generateMesh.py " + workPath.salome_path)
