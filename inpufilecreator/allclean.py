"""
This code is used to clean working tree.
All the input files, expect the mesh file, will be deleted.
email hui.cheng@uis.no
"""
import os
import sys

inputkey = input("\nPlease make sure you want to clean working tree, or press 'CTRL+C' to exit")
os.system("mv /inputfiles/*.med ")
os.system("rm -rf asterinput/ ")
os.system("rm -rf asteroutput/ ")
