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
if len(sys.argv)<2:
    print("Please add a argument when using this command")
    exit()
os.system("python3 " + workPath.inputcreater_path + "inputModule.py " + str(sys.argv[1]))
