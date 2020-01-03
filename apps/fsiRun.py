"""
writer hui cheng
email hui.cheng@uis.no
"""
import os
import workPath
import time

with open('cageDict', 'r') as f:
    content = f.read()
    cageinfo = eval(content)

cwd = os.getcwd()
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

os.system("python3 " + workPath.inputcreater_path + "CM_" + cageinfo['Weight']['weightType'] + ".py")

print("\n"
      "\n"
      "Currently, this code is not ready for release\n"
      "Any questions about this code, please email: hui.cheng@uis.no")
time.sleep(0.5)
os.system("python3 " + workPath.app_path + "fsi_mapCoorAndFh.py")

print("source " + workPath.aster_path)
# os.system("source " + workPath.aster_path)
os.system("as_run ./asterinput/ASTERRUN.export")
