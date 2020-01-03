import os
import sys

# from scr.Meshcreater import dictCheaker as dc
import dictCheaker as dc
import workPath

Dictname = str(sys.argv[1])

with open(Dictname, 'r') as f:
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
    'threecages'
]  # add more models if it is ready
if cageinfo['CageShape']['shape'] in cageTypes:
    dc.check(cageinfo, cageinfo['CageShape']['shape'])
    os.system(str(workPath.salome_path) + " -t " + workPath.mesh_path + "ME_" + cageinfo['CageShape'][
        'shape'] + ".py " + "args:" + Dictname)
else:
    printmodel()
    exit()
