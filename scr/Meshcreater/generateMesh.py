import os
import sys
# from scr.Meshcreater import dictCheaker as dc
import dictCheaker as dc
import workPath
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


if cageinfo['cageType'] in modelList:
    dc.check(cageinfo, cageinfo['cageType'])
    os.system(str(sys.argv[1]) + " -t " + workPath.mesh_path + "ME_" + cageinfo['cageType'] + ".py")
else:
    printmodel()
    exit()
