import os
import sys
import workPath

if len(sys.argv) < 2:
    print("\nNo input dictionary file. \n"
          "Usage: aquaMesh + [dictionary name]\n"
          "i.e., aquaMesh cage1\n"
          "The dictionary file follows the Python's syntax.\n ")
    exit()
os.system("python3 " + workPath.mesh_path + "generateMesh.py " + str(sys.argv[1]))
