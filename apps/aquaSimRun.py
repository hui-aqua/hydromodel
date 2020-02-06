"""
/--------------------------------\
|    University of Stavanger     |
|           Hui Cheng            |
\--------------------------------/
Any questions about this code, please email: hui.cheng@uis.no

"""
import os
import workPath

cwd = os.getcwd()
print("\nThe working folder is ' " + str(cwd) + " ' \n")

if not os.path.exists("asterinput"):
    os.mkdir("asterinput")
if not os.path.exists("asteroutput"):
    os.mkdir("asteroutput")
files = os.listdir(cwd)
for file in files:
    if file.endswith(".med") or file.endswith(".txt") or file.endswith(".comm") or file.endswith(".export") :
        os.rename(os.path.join(cwd, file), os.path.join(os.path.join(cwd, "asterinput"), file))
print("\n"
      "Remember to source your Code_Aster before running simulations.\n"
      "i.e., source " + workPath.aster_path + "\n"
                                              "Any questions about this code, please email: hui.cheng@uis.no")
os.system("source " + workPath.aster_path)
os.system("as_run ./asterinput/ASTERRUN.export")
