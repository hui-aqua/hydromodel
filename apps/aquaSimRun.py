"""
/--------------------------------\
|    University of Stavanger     |
|           Hui Cheng            |
\--------------------------------/
Any questions about this code, please email: hui.cheng@uis.no

"""
import os
import sys
import workPath
import time
import ast
if len(sys.argv) < 2:
    print("\nPlease add a argument when using this command.\n"
          "Usage: aquaAster + [dictionary name]\n")
    exit()
with open(str(sys.argv[1]), 'r') as f:
    content = f.read()
    cageInfo = ast.literal_eval(content)

meshLib = str(cageInfo['MeshLib'])
os.system("python3 " + workPath.inputcreater_path + "AS_"+meshLib+".py " + str(sys.argv[1]) )
time.sleep(1)


cwd = os.getcwd()
print("\nThe working folder is ' " + str(cwd) + " ' \n")
print("Please make sure the working path locates ./constant, if you want to do FSI simulation")
file_names = ['ASTER2.py', 'ASTER1.py', 'meshInformation.py']


def run_simulation():
    if not os.path.exists("asterinput"):
        os.mkdir("asterinput")
    if not os.path.exists("asteroutput"):
        os.mkdir("asteroutput")
    if not os.path.exists("positionOutput"):
        os.mkdir("positionOutput")
    if not os.path.exists("midOutput"):
        os.mkdir("midOutput")
    if not os.path.exists("midOutput/REPE_OUT"):
        os.mkdir("midOutput/REPE_OUT")
    files = os.listdir(cwd)
    for file in files:
        if file.endswith(".med") or file in file_names or file.endswith(".export"):
            os.rename(os.path.join(cwd, file), os.path.join(os.path.join(cwd, "asterinput"), file))
    print("\n"
          "Remember to source your Code_Aster before running simulations.\n"
          "i.e., source /opt/aster144/etc/codeaster/profile.sh \n"
          "Any questions about this code, please email: hui.cheng@uis.no")
    os.system("as_run " + os.path.join(cwd, 'asterinput/ASTERRUN.export'))


run_simulation()
