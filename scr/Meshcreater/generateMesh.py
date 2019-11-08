import os
import sys
import dictCheaker as dc

with open('cagedict', 'r') as f:
    content = f.read()
    cageinfo = eval(content)

modelList = [
    "fishcagewithbottom",
    "fishcagewithoutbottom",
    "squarefishcage",
    "trawlnet",
    "fishcagewithmooringsystem"]  # add more models if it is ready


def printmodel():
    print("The cage type '" + cageinfo['cageType'] + "' are not included in this code.\n")
    print("Currently, the available numerical models are:")
    for model in modelList:
        print(str(modelList.index(model)) + " " + model)


modelBank = "/home/hui/GitCode/aqua/scr/Meshcreater/"  # todo autochange the parth in install.py

if cageinfo['cageType'] in modelList:
    dc.check(cageinfo, cageinfo['cageType'])
    os.system(str(sys.argv[1]) + " -t " + modelBank + "ME_" + cageinfo['cageType'] + ".py")
else:
    printmodel()
    exit()
