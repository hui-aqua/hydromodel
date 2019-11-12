"""
writer hui cheng
email hui.cheng@uis.no
"""
import os
import workPath
import time
with open('cagedict', 'r') as f:
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

os.system("python3 " + workPath.inputcreater_path + "CM_" + cageinfo['cageType'] + ".py")

print("\n"
      "\n"
      "Currently, this code is not ready for release\n"
      "Any questions about this code, please email: hui.cheng@uis.no")
time.sleep(4.5)

os.system("source /opt/aster144/etc/codeaster/profile.sh")
os.system("as_run ./asterinput/ASTERRUN.export")
