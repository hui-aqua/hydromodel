"""
/--------------------------------\
|    University of Stavanger     |
|           Hui Cheng            |
\--------------------------------/
Any questions about this code, please email: hui.cheng@uis.no
The center of the floating collar is (0,0,0)
Fish cage is along the Z- direction
Z=0 is the free surface
Z<0 is the water zone
Z>0 is the air zone
STB means the weights include sinkers+sinker tube+bottom
The sinkers are attached to the floating collar
"""

import sys
import os
import numpy as np
from numpy import pi
import ast

point = [] # points on netting
con = []   # lines on netting
sur = []   # surface on netting
mcon = []  # lines on mooring
wcon = []  # lines on weight lines
cwd = os.getcwd()

with open(str(sys.argv[1]), 'r') as f:
    content = f.read()
    cageInfo = ast.literal_eval(content)

NT = cageInfo['CageShape']['elementOverCir']  # Number of the nodes in circumference
NN = cageInfo['CageShape']['elementOverHeight']  # number of section in the height, thus, the nodes should be NN+1
floater_center = cageInfo['FloatingCollar']['floaterCenter']
D = cageInfo['CageShape']['cageDiameter']
H = cageInfo['CageShape']['cageHeight']

# generate the point coordinates matrix for cylindrical cage
for j in range(0, NN + 1):
    for i in range(0, NT):
        point.append(
            [floater_center[0] + D / 2 * np.cos(i * 2 * pi / float(NT)),
             floater_center[1] + D / 2 * np.sin(i * 2 * pi / float(NT)),
             floater_center[2] - j * H / float(NN)])

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> salome
# the below is the commond in the Mesh, Salome.
# the mesh creater script
import salome

salome.salome_init()
theStudy = salome.myStudy
import SMESH
from salome.smesh import smeshBuilder

smesh = smeshBuilder.New(theStudy)
Mesh_1 = smesh.Mesh()

# add the pints into geometry
for each_node in point:
    nodeID = Mesh_1.AddNode(float(each_node[0]), float(each_node[1]), float(each_node[2]))

for i in range(1, NT + 1):
    for j in range(0, NN + 1):
        # the last horizontal line
        if j == NN:
            if i == NT:
                edge = Mesh_1.AddEdge([i + j * NT,
                                       1 + i + (j - 1) * NT])  # add the horizontal line into geometry
                con.append([i + j * NT - 1,
                            1 + i + (j - 1) * NT - 1])  # add the horizontal line into con
            else:
                edge = Mesh_1.AddEdge([i + j * NT,
                                       1 + i + j * NT])  # add the horizontal line into geometry
                con.append([i + j * NT - 1,
                            1 + i + j * NT - 1])  # add the horizontal line into con
        # the rest lines and all vertical surfaces
        else:
            edge = Mesh_1.AddEdge([i + j * NT, i + (j + 1) * NT])  # add the vertical line into geometry
            con.append([i + j * NT - 1, i + (j + 1) * NT - 1])  # add the vertical line into con
            if i == NT:
                edge = Mesh_1.AddEdge([i + j * NT, 1 + i + (j - 1) * NT])  # add the horizontal line into geometry
                con.append([i + j * NT - 1, 1 + i + (j - 1) * NT - 1])  # add the horizontal line into con
                sur.append([i + j * NT - 1,
                            1 + i + (j - 1) * NT - 1,
                            i + (j + 1) * NT - 1,
                            1 + i + j * NT - 1])
            else:
                edge = Mesh_1.AddEdge([i + j * NT, 1 + i + j * NT])  # add the horizontal line into geometry
                con.append([i + j * NT - 1, 1 + i + j * NT - 1])  # add the horizontal line into con
                sur.append([i + j * NT - 1,
                            1 + i + j * NT - 1,
                            i + (j + 1) * NT - 1,
                            1 + i + (j + 1) * NT - 1])

if "Tube" in cageInfo["Weight"]["weightType"] and float(cageInfo["Weight"]["bottomRingDepth"]) != float(H):
    # sinkerTube is added at the bottom.
    bottomRingDepth = float(cageInfo["Weight"]["bottomRingDepth"])
    for i in range(NT):
        point.append(
            [floater_center[0] + D / 2 * np.cos(i * 2 * pi / float(NT)),
             floater_center[1] + D / 2 * np.sin(i * 2 * pi / float(NT)),
             floater_center[2] - bottomRingDepth])
        nodeID = Mesh_1.AddNode(float(floater_center[0] + D / 2 * np.cos(i * 2 * pi / float(NT))),
                                float(floater_center[1] + D / 2 * np.sin(i * 2 * pi / float(NT))),
                                float(floater_center[2] - bottomRingDepth))
    for i in range(1, NT + 1):
        if bottomSwitcher in ['WithBottom']:
            edge = Mesh_1.AddEdge([len(point) - i + 1, len(point) - i - NT])  # add the vertical line into geometry
            con.append([len(point) - i, len(point) - i - NT - 1])  # add the vertical line into con
        else:
            edge = Mesh_1.AddEdge([len(point) - i + 1, len(point) - i - NT + 1])  # add the vertical line into geometry
            con.append([len(point) - i, len(point) - i - NT])  # add the vertical line into con
        if i == NT:
            edge = Mesh_1.AddEdge([len(point), len(point) - NT + 1])  # add the horizontal line into geometry
            con.append([len(point) - 1, len(point) - NT])  # add the horizontal line into con
        else:
            edge = Mesh_1.AddEdge([len(point) - i + 1, len(point) - i])  # add the horizontal line into geometry
            con.append([len(point) - i, len(point) - i - 1])  # add the horizontal line into con

isDone = Mesh_1.Compute()
# naming  the group
# GROUP_NO
allnodes = Mesh_1.CreateEmptyGroup(SMESH.NODE, 'allnodes')
nbAdd = allnodes.AddFrom(Mesh_1.GetMesh())
smesh.SetName(allnodes, 'allnodes')

# define the topnodes, the reaction forces are calculated based on topnodes.
topnodes = Mesh_1.CreateEmptyGroup(SMESH.NODE, 'topnodes')
nbAdd = topnodes.Add([i for i in range(NT + 1)])
smesh.SetName(topnodes, 'topnodes')

# define the nodes on bottom ring
bottomnodes = Mesh_1.CreateEmptyGroup(SMESH.NODE, 'bottomnodes')
nbAdd = bottomnodes.Add([i for i in range(NT * NN + 1, NT * (NN + 1) + 1)])
smesh.SetName(bottomnodes, 'bottomnodes')

# define the nodes for sinkers
if cageInfo['Weight']['weightType'] in ['sinkers']:
    NS = float(cageInfo['Weight']['numOfSinkers'])
    if (float(cageInfo['CageShape']['elementOverCir']) / NS).is_integer():
        print("\nThe sinkers are evenly distributed in the bottom.")
        sinkers = Mesh_1.CreateEmptyGroup(SMESH.NODE, 'sinkers')
        nbAdd = sinkers.Add(
            [i for i in range(len(point) - NT + 1, len(point),
                              int(cageInfo['CageShape']['elementOverCir'] / NS))])
        smesh.SetName(sinkers, 'sinkers')
    else:
        print("\nThe sinkers can not be evenly distributed in the bottom."
              "\nYou need to add the sinker manually.")
else:
    print("\nThere is no sinkers on the bottom ring")

# generate the name for each node to assign the hydrodynamic forces.
for i in range(1, len(point) + 1):
    node1 = Mesh_1.CreateEmptyGroup(SMESH.NODE, 'node%s' % i)
    nbAdd = node1.Add([i])
    smesh.SetName(node1, 'node%s' % i)

if "centerweight" in cageInfo['Weight']['weightType']:
    node1 = Mesh_1.CreateEmptyGroup(SMESH.NODE, 'bottom_tit')
    nbAdd = node1.Add([len(point) - NT])
    smesh.SetName(node1, 'bottom_tit')

# GROUP_MA
# defaults names for all the twines and nodes.
twines = Mesh_1.CreateEmptyGroup(SMESH.EDGE, 'twines')
nbAdd = twines.AddFrom(Mesh_1.GetMesh())
smesh.SetName(twines, 'twines')

# the top ring to keep ths shape of the fish cage.
topring = Mesh_1.CreateEmptyGroup(SMESH.EDGE, 'topring')
nbAdd = topring.Add([i for i in range(2, NT * (2 * NN + 1), 2 * NN + 1)])
smesh.SetName(topring, 'topring')

# bottom ring will keep the cage and add the sink forces
bottomring = Mesh_1.CreateEmptyGroup(SMESH.EDGE, 'bottomring')
nbAdd = bottomring.Add([i for i in range(2 * NN + 1, (NT + 1) * (2 * NN + 1), 2 * NN + 1)])
smesh.SetName(bottomring, 'bottomring')

# give a name to the mesh
meshname = "single_cage_" + str(sys.argv[1]).split('.')[0] + ".med"
Mesh_1.ExportMED(cwd + "/" + meshname)

lineinfo = {

}

meshinfo = {
    "horizontalElementLength": float(pi * D / float(NT)),
    "verticalElementLength": float(H / float(NN)),
    "numberOfNodes": len(point),
    "numberOfLines": len(con),
    "numberOfSurfaces": len(sur),
    "netLines": con,
    "mooringLines": mcon,
    "weightLines": wcon,
    "netSurfaces": sur,
    "netNodes": point,
    "NN": NN,
    "NT": NT,
    "meshName": meshname
}
print("\n"
      "  --------------------------------------\n"
      "  --     University of Stavanger      --\n"
      "  --         Hui Cheng (PhD student)  --\n"
      "  --       Lin Li (Medveileder)       --\n"
      "  --  Prof. Muk Chen Ong (supervisor) --\n"
      "  --------------------------------------\n"
      "  Any questions about this code,\n"
      "  please email: hui.cheng@uis.no\n"
      "  Net panel(s)")
print("<<<<<<<<<< Mesh Information >>>>>>>>>>")
print("Number of node is " + str(meshinfo["numberOfNodes"]) + ".")
print("Number of line element is " + str(meshinfo["numberOfLines"]) + ".")
print("Number of surface element is " + str(meshinfo["numberOfSurfaces"]) + ".\n")

with open(cwd + "/meshInformation.py", 'w') as f:
    f.write("meshinfo=")
    f.write(str(meshinfo))
f.close()
