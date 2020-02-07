"""
/--------------------------------\
|    University of Stavanger     |
|           Hui Cheng            |
\--------------------------------/
Any questions about this code, please email: hui.cheng@uis.no

"""
import os
import workPath
import sys
import ast

with open(str(sys.argv[1]), 'r') as f:
    content = f.read()
    cageInfo = ast.literal_eval(content)

cwd = os.getcwd()
print("\nThe working folder is ' " + str(cwd) + " ' \n")


def run_simulation():
    if not os.path.exists("asterinput"):
        os.mkdir("asterinput")
    if not os.path.exists("asteroutput"):
        os.mkdir("asteroutput")
    files = os.listdir(cwd)
    for file in files:
        if file.endswith(".med") or file.endswith(".txt") or file.endswith(".comm") or file.endswith(".export"):
            os.rename(os.path.join(cwd, file), os.path.join(os.path.join(cwd, "asterinput"), file))
    print("\n"
          "Remember to source your Code_Aster before running simulations.\n"
          "i.e., source " + workPath.aster_path + "\n"
                                                  "Any questions about this code, please email: hui.cheng@uis.no")
    os.system("source " + workPath.aster_path)
    os.system("as_run " + os.path.join(cwd, 'asterinput/ASTERRUN.export'))


if cageInfo['Solver']['coupling'] in ['False']:
    run_simulation()
elif cageInfo['Solver']['coupling'] in ['simiFSI', 'FSI']:
    if cwd.split('/')[-1] not in ['constant']:
        print("\nError!!! Please prepare the OpenFOAM input file first. And run the Code_Aster in constant")
        exit()
    else:
        run_simulation()
