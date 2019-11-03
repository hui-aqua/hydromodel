"""
writer hui cheng
email hui.cheng@uis.no
"""
import os
import time
import sys
sys.path.append(
    '/home/hui/GitCode/aqua/scr/inpufilecreator'
)
import creamodule as cme
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
cme.CR_comm(cwd)
cme.CR_export(cwd, meshfile)
print("\n"
      "\n"
      "Currently, this code is not ready for release\n"
      "Any questions about this code, please email: hui.cheng@uis.no")
time.sleep(1.5)
os.system("source /opt/aster144/etc/codeaster/profile.sh")
os.system("as_run ./asterinput/ASTERRUN.export")
