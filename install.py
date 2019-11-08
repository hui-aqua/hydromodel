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
