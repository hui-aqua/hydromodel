"""
This code is used to clean working tree.
All the input files, expect the mesh file, will be deleted.
email hui.cheng@uis.no
"""
import os
import shutil

cwd = os.getcwd()
print("\nPlease make sure you want to clean working tree, ALL the relevant files will be removed \n")
files_need_clean = ['Fh', 'posi', 'surf']
folders_need_clean = ['asteroutput', 'asterinput']
for file in files_need_clean:
    if os.path.isfile(os.path.join(cwd, file)):
        os.remove(file)
    else:
        print("The file '" + str(file) + "' does not exist in the work path.")

for folder in folders_need_clean:
    if os.path.isdir(os.path.join(cwd, folder)):
        shutil.rmtree(folder)
    else:
        print("The folder '" + str(folder) + "' does not exist in the work path.")

files = os.listdir(cwd)
for file in files:
    if file.endswith(".txt") or file.endswith(".comm") or file.endswith(".med") or file.endswith(".export"):
        os.remove(os.path.join(cwd, file))
