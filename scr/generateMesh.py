import os
import sys
# from scr.Meshcreater import dictCheaker as dc
from Meshcreater import dictCheaker as dc
import workPath

with open('cageDict', 'r') as f:
    content = f.read()
    cageinfo = eval(content)

def printmodel():
    print("The cage type '" + cageinfo['CageShape']['CageType'] + "' are not included in this version.\n")

    print("Currently, the available numerical models are:")
    for model in cageTypes:
        print(str(cageTypes.index(model)) + " " + model)


cageTypes = [
    "cylindricalNoBottom",
    "cylindricalWithBottom",
    "squaredNoBottom",
    "squaredWithBottom",
    "cylindricalWithBottomWithMooring",
    "trawlnet",
]  # add more models if it is ready
if cageinfo['CageShape']['CageType'] in cageTypes:
    dc.check(cageinfo, cageinfo['CageShape'])
    os.system(str(sys.argv[1]) + " -t " + workPath.mesh_path + "ME_" + cageinfo['cageType'] + ".py")
else:
    printmodel()
    exit()
