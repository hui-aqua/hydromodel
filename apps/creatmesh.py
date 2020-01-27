
import os
import sys
import workPath
if len(sys.argv)<2:
    print("Please add a argument when using this command")
    exit()
os.system("python3 " + workPath.mesh_path + "generateMesh.py " + str(sys.argv[1]))
