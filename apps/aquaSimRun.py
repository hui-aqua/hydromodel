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
print("\nThe working folder is ' "+str(cwd)+ " ' \n")

if not os.path.exists("asterinput"):
    os.mkdir("asterinput")
if not os.path.exists("asteroutput"):
    os.mkdir("asteroutput")
files = os.listdir(cwd)
for i in files:
    if os.path.splitext(i)[1] == ".med":
        meshfile = str(i)
os.system("mv *.txt ./asterinput/")
os.system("mv *.med ./asterinput/")
os.system("mv *.comm ./asterinput/")
os.system("mv *.export ./asterinput/")
print("\n"
      "Remember to source your Code_Aster before running simulations.\n"
      "i.e., source " + workPath.aster_path+"\n"
      "Any questions about this code, please email: hui.cheng@uis.no")
os.system("source " + workPath.aster_path)
os.system("as_run ./asterinput/ASTERRUN.export")

