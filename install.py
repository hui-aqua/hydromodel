import os

cwd = os.getcwd()
output_file = open('./etc/aliases.sh', 'w')
output_file.write('''
# Description
#     Aliases for working with Code_Aster
# hui.cheng@uis.no
export APP=''' + cwd + '''
alias amesh='python3 $APP/apps/creatmesh.py'
alias arun='python3 $APP/apps/allrun.py'
alias aclean='python3 $APP/apps/allclean.py'
    \n''')
output_file.write('\n')
output_file.close()

output_file = open('./etc/workPath.py', 'w')
output_file.write("""
'''
 Description
     workingPath for code in ./apps,
     scr/meshcreater and scr/imputfilecreator.
     Soft link is created in the above folders.
 hui.cheng@uis.no
'''
Program_path = "''' + cwd + '''"
mesh_path = Program_path+"/scr/Meshcreater/"
inputcreater_path = Program_path+"/scr/inputfilecreator/"
forceModel_path = Program_path+"/scr/forcemodel/"
    \n""")
output_file.write('\n')
output_file.close()
os.system("ln -sf " + cwd + "/etc/workPath.py ./scr/inputfilecreator/workPath.py")
os.system("ln -sf " + cwd + "/etc/workPath.py ./scr/Meshcreater/workPath.py")
os.system("ln -sf " + cwd + "/etc/workPath.py ./apps/workPath.py")
