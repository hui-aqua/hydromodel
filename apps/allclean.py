"""
This code is used to clean working tree.
All the input files, expect the mesh file, will be deleted.
email hui.cheng@uis.no
"""
import os

print("\nPlease make sure you want to clean working tree, ALL the relevant files will be removed \n")
os.system("echo -n 'Press any key to continue or 'CTRL+C' to exit : \n'")
os.system("read var_name")
os.system("rm -rf asterinput/ ")
os.system("rm -rf asteroutput/ ")
os.system("rm -rf *.txt ")
os.system("rm -rf *.med ")
os.system("rm -rf *.comm ")
os.system("rm -rf *.export ")
