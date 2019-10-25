"""
this is a input file creator for code aster
writer hui cheng
email hui.cheng@uis.no
"""
import os
import sys
sys.path.append(
    '/home/hui/GitCode/AllCodeRepository/coderepository/CodeAsterModule/inputfilescreator'
)
import creamodule as cme
cme.Sn = 0.194     # net solidity
cme.dw = 2.42e-3   # [m] net twine diameter
cme.a = 0.0255     # [m] net half mesh length
cme.weight = 4.48  # [N] weight
cme.E = 40000000   # [Pa] Y M
cme.refa = 0.886   # flow reduction factor

cwd = os.getcwd()
os.mkdir("resufiles")
os.mkdir("initialcondition")
os.mkdir("inputfiles")
Hydrodynamicmodel = 'Fh4'
FileName1 = "test" + Hydrodynamicmodel + ".comm"
FileName2 = "test" + Hydrodynamicmodel + ".export"
cme.CR_comm(FileName1, cwd, Hydrodynamicmodel)
cme.CR_export(FileName2, FileName1, cwd)
cme.CR_shscript(FileName2)
os.system("gnome-terminal -- bash runit.sh")
os.remove("runit.sh")
