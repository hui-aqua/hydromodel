#!/usr/bin/env python
import os
import sys
import workPath
from etc import workPath
os.system("python3 " + workPath.mesh_path + "generateMesh.py " + str(sys.argv[1]))
