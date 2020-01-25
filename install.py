import os

os.system("clear")
cwd = os.getcwd()
salomePath = input(
    "The default path for salome2019 is: \t/opt/salome2019/appli_V2019_univ/salome \n"
    "If your salome is located in this path, you can press '1' and enter \n\n"
    "The default path for salome2018 is: \t/opt/salome2018/appli_V2018.0.1_public/salome \n"
    "If your salome is located in this path, you can press '2' and enter \n\n"
    "Please input you path to salome in your computer \n")
if salomePath == str(1):
    salomePath = "/opt/salome2019/appli_V2019_univ/salome"
if salomePath == str(2):
    salomePath = "/opt/salome2018/appli_V2018.0.1_public/salome"
while not os.path.isfile(salomePath):
    salomePath = input("Sorry, I cannot find salome in your given path, please input it again \n")
    if salomePath == str(1):
        salomePath = "/opt/salome2019/appli_V2019_univ/salome"
    if salomePath == str(2):
        salomePath = "/opt/salome2018/appli_V2018.0.1_public/salome"
os.system("clear")
asterPath = input("Please add the path of 'profile.sh' to your code_aster in your computer\n"
                  "The default path for code_aster 14.2 is: \t /opt/aster/etc/codeaster/profile.sh \n"
                  "If you want to use cod_aster 14.2, you can press '1' and enter \n\n"
                  "The default path for code_aster 14.4 is \t /opt/aster144/etc/codeaster/profile.sh\n"
                  "If you want to use cod_aster 14.4, you can press '2' and enter \n\n"
                  "If the two default path is not applied to your computer, you can input your own path and enter \n")

if asterPath == str(1):
    asterPath = "/opt/aster/etc/codeaster/profile.sh"
if asterPath == str(2):
    asterPath = "/opt/aster144/etc/codeaster/profile.sh"
while not os.path.isfile(asterPath):
    asterPath = input("Sorry, I cannot find salome in your given path, please input it again \n")
    if asterPath == str(1):
        asterPath = "/opt/aster/etc/codeaster/profile.sh"
    if asterPath == str(2):
        asterPath = "/opt/aster144/etc/codeaster/profile.sh"

output_file = open('./etc/aliases.sh', 'w')
output_file.write('''
# Description
#     Aliases for working with Code_Aster
# hui.cheng@uis.no
export APP=''' + cwd + '''
alias amesh='python3 $APP/apps/creatmesh.py'
alias arun='python3 $APP/apps/arun.py'
alias brun='python3 $APP/apps/brun.py'
alias crun='python3 $APP/apps/crun.py'
alias aclean='python3 $APP/apps/allclean.py'
alias aqua-version='python3 $APP/apps/aqua-version.py'
    
    \n''')
output_file.write('\n')
output_file.close()

output_file = open('./etc/workPath.py', 'w')
output_file.write('''
# Description
#     workingPath for code in ./apps,
#     scr/meshcreater and scr/imputfilecreator.
#     Soft link is created in the above folders.
# hui.cheng@uis.no

Program_path = "''' + cwd + '''"
scr_path = Program_path+"/scr/"
mesh_path = Program_path+"/scr/Meshcreater/"
inputcreater_path = Program_path+"/scr/inputfilecreator/"
forceModel_path = Program_path+"/scr/forcemodel/"
seawave_path = Program_path+"/scr/enviroments/"
app_path= Program_path+"/apps/"
salome_path = "''' + salomePath + '''"
aster_path = "''' + asterPath + '''"
    \n''')
output_file.write('\n')
output_file.close()
os.system("ln -sf " + cwd + "/etc/workPath.py ./scr/inputfilecreator/workPath.py")
os.system("ln -sf " + cwd + "/etc/workPath.py ./scr/Meshcreater/workPath.py")
os.system("ln -sf " + cwd + "/etc/workPath.py ./scr/forcemodel/workPath.py")
os.system("ln -sf " + cwd + "/etc/workPath.py ./apps/workPath.py")

