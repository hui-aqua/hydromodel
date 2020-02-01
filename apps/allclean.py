"""
This code is used to clean working tree.
All the input files, expect the mesh file, will be deleted.
email hui.cheng@uis.no
"""
import os
import shutil

cwd = os.getcwd()
try:
    os.remove("ASTERRUN.export")
except:
    print("Error while deleting file : ASTERRUN.export")
print("\nPlease make sure you want to clean working tree, ALL the relevant files will be removed \n")

# os.removexattr()
# os.remove("*.txt")
# os.system("rm -rf *.txt ")
# os.system("rm -rf *.med ")
# os.system("rm -rf *.comm ")
# os.system("rm -rf *.export ")

try:
    shutil.rmtree("asteroutput")
except:
    print("asteroutput does not exist here or have no permission to remove it.")

try:
    shutil.rmtree("asterinput")
except:
    print("asterinput does not exist here or have no permission to remove it.")
try:
    os.remove("Fh")
except:
    print("Fh does not exist here or have no permission to remove it.")

try:
    os.remove("posi")
except:
    print("posi does not exist here or have no permission to remove it.")
try:
    os.remove("surf")
except:
    print("surf does not exist here or have no permission to remove it.")
