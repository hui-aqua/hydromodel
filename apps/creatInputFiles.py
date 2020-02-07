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
if len(sys.argv) < 2:
    print("\nPlease add a argument when using this command.\n"
          "Usage: aquaAster + [dictionary name]\n")
    exit()
os.system("python3 " + workPath.inputcreater_path + "inputModule.py " + str(sys.argv[1]) )
time.sleep(1)
print("\nALL finished! You can check the input file manually and run 'aquaSim' to start the simulation\n")