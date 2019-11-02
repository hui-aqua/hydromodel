"""
this is a input file creator for code aster
writer hui cheng
email hui.cheng@uis.no
"""
import os
import sys
sys.path.append(
    '/home/hui/GitCode/aqua/scr/inpufilecreator'
)
import creamodule as cme

cwd = os.getcwd()
os.mkdir("resufiles")
os.mkdir("inputfiles")
os.system("mv lines.txt ./inputfiles/")
os.system("mv surfaces.txt ./inputfiles/")
os.system("mv *.med ./inputfiles/")

FileName1 = "test.comm"
FileName2 = "test.export"
cme.CR_comm(FileName1, cwd)
cme.CR_export(FileName2, FileName1, cwd)
cme.CR_shscript(FileName2)
