import os
from etc import workPath
os.system("clear")
if not os.path.isfile('cagedict'):
    print("\n Please make sure cagedict is located in the working path.\n")
    exit()

apPath = input(
    "The default path for salome2019 is: \t/opt/salome2019/appli_V2019_univ/salome \n"
    "If your salome is located in this path, you can press '1' and enter \n\n"
    "The default path for salome2018 is: \t/opt/salome2018/appli_V2018.0.1_public/salome \n"
    "If your salome is located in this path, you can press '2' and enter \n\n"
    "Please input you path to salome in your computer \n")
if apPath == str(1):
    apPath = "/opt/salome2019/appli_V2019_univ/salome"
if apPath == str(2):
    apPath = "/opt/salome2018/appli_V2018.0.1_public/salome"
while not os.path.isfile(apPath):
    apPath = input("Sorry, I cannot find salome in your given path, please input it again \n")
    if apPath == str(1):
        apPath = "/opt/salome2019/appli_V2019_univ/salome"
    if apPath == str(2):
        apPath = "/opt/salome2018/appli_V2018.0.1_public/salome"
os.system("clear")

os.system("python3 " + workPath.mesh_path + "generateMesh.py " + apPath)
