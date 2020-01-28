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

if len(sys.argv) < 3:
    print("\nPlease add 2 arguments when using this command.\n"
          "Usage: aquaAster + [dictionary name] + [option]\n"
          "Available option:\n"
          "1. FE\n"
          "2. FSI\n"
          "3. simiFSI\n")
    exit()
os.system("python3 " + workPath.inputcreater_path + "inputModule.py " + str(sys.argv[1]) + str(sys.argv[2]))
