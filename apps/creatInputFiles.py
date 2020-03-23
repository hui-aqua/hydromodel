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
import time
import ast
if len(sys.argv) < 2:
    print("\nPlease add a argument when using this command.\n"
          "Usage: aquaAster + [dictionary name]\n")
    exit()
with open(str(sys.argv[1]), 'r') as f:
    content = f.read()
    cageInfo = ast.literal_eval(content)

meshLib = str(cageInfo['MeshLib'])
os.system("python3 " + workPath.inputcreater_path + "AS_"+meshLib+".py " + str(sys.argv[1]) )
time.sleep(1)
