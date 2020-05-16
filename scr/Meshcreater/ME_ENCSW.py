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
STB means the weights include sinkers+sinker
The sinkers are attached to the floating collar
"""

import sys
import os
import numpy as np
from numpy import pi
import ast

point = []  # points on netting
con = []  # lines on netting
sur = []  # surface on netting
mcon = []  # lines on mooring
wcon = []  # lines on weight lines
cwd = os.getcwd()

with open(str(sys.argv[1]), 'r') as f:
    content = f.read()
    cageInfo = ast.literal_eval(content)

NT = cageInfo['CageShape']['elementOverCir']  # Number of the nodes in circumference
NN = cageInfo['CageShape']['elementOverHeight']  # number of section in the height, thus, the nodes should be NN+1
BN = cageInfo['CageShape']['elementOverCone']  # number of section along the cone, thus, the nodes should be NN+1
floater_center = cageInfo['FloatingCollar']['floaterCenter']
cage_diameter = cageInfo['CageShape']['cageDiameter']
cage_height = cageInfo['CageShape']['cageHeight']
cage_cone_height = cageInfo['CageShape']['cageConeHeight']
number_of_sinker = cageInfo['Weight']['numOfSinkers']

# generate the point coordinates matrix for cylindrical cage
for j in range(0, NN + 1):
    for i in range(0, NT):
        point.append(
            [floater_center[0] + cage_diameter / 2 * np.cos(i * 2 * pi / float(NT)),
             floater_center[1] + cage_diameter / 2 * np.sin(i * 2 * pi / float(NT)),
             floater_center[2] - j * cage_height / float(NN)])

for j in range(1, BN):
    for i in range(0, NT):
        point.append(
            [floater_center[0] + cage_diameter / 2 * ((BN - j) / BN) * np.cos(i * 2 * pi / float(NT)),
             floater_center[1] + cage_diameter / 2 * ((BN - j) / BN) * np.sin(i * 2 * pi / float(NT)),
             floater_center[2] - cage_height - j * (cage_cone_height - cage_height) / float(BN)])

point.append([floater_center[0], floater_center[1], -cage_cone_height])  # the last point should be at the cone tip
net_node_number = len(point)

# point for weight
for j in range(0, NN + 2):
    for i in range(number_of_sinker):
        point.append([floater_center[0] + (cage_diameter / 2 + float(cageInfo['FloatingCollar']['DistPipes'])) * np.cos(
            i * 2 * pi / float(number_of_sinker)),
                      floater_center[1] + (cage_diameter / 2 + float(cageInfo['FloatingCollar']['DistPipes'])) * np.sin(
                          i * 2 * pi / float(number_of_sinker)),
                      floater_center[2] - j * float(cageInfo['Weight']['sinkerDepth']) / float(NN + 1)])
weight_node_number = len(point) - net_node_number

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
# >>>>>>>>>>
# Netting line and surface
# >>>>>>>>>>
for i in range(1, NT + 1):
    for j in range(0, BN + NN):
        # the last horizontal line
        if j == BN + NN - 1:
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
                edge = Mesh_1.AddEdge([i + j * NT,
                                       1 + i + (j - 1) * NT])  # add the horizontal line into geometry
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

# the last line and surf(triangular surf)
for i in range(1, NT + 1):
    edge = Mesh_1.AddEdge([net_node_number, net_node_number - i])  # add the horizontal line into geometry
    con.append([net_node_number - 1, net_node_number - i - 1])  # add the horizontal line into con
    if i == NT:
        sur.append([net_node_number - 1,
                    net_node_number - i - 1,
                    net_node_number - 2])
    else:
        sur.append([net_node_number - 1,
                    net_node_number - i - 1,
                    net_node_number - i - 2])

# >>>>>>>>>>
# support lines
# >>>>>>>>>>
# horizontal line at top
# for i in range(number_of_sinker):
#     if i == number_of_sinker-1:
#         edge = Mesh_1.AddEdge([net_node_number + 1 + i, net_node_number + 1])  # add the vertical line into geometry
#         wcon.append([net_node_number + i, net_node_number])
#     else:
#         edge = Mesh_1.AddEdge([net_node_number+1+i,net_node_number+2+i])  # add the vertical line into geometry
#         wcon.append([net_node_number+i,net_node_number+1+i])
#


# vertical lines
for i in range(number_of_sinker):
    for j in range(NN + 1):
        edge = Mesh_1.AddEdge([net_node_number + i + 1 + j * number_of_sinker,
                               net_node_number + i + 1 + (
                                           j + 1) * number_of_sinker])  # add the vertical line into geometry
        wcon.append([net_node_number + i,
                     net_node_number + i + j * number_of_sinker])

# horizontal lines at bottom
trick = [[193, 394 + 8], [197, 395 + 8], [201, 396 + 8], [205, 397 + 8], [209, 398 + 8], [213, 399 + 8], [217, 400 + 8],
         [221, 401 + 8]]
for line in trick:
    edge = Mesh_1.AddEdge(line)  # add the vertical line into geometry
    wcon.append([line[0] - 1, line[1] - 1])

isDone = Mesh_1.Compute()

# naming  the group
# naming the node
# GROUP_NO
allnodes = Mesh_1.CreateEmptyGroup(SMESH.NODE, 'allnodes')
nbAdd = allnodes.AddFrom(Mesh_1.GetMesh())
smesh.SetName(allnodes, 'allnodes')

# define the topnodes, the reaction forces are calculated based on topnodes.
topnodes = Mesh_1.CreateEmptyGroup(SMESH.NODE, 'topnodes')
nbAdd = topnodes.Add([i for i in range(NT + 1)])
nbAdd = topnodes.Add([i for i in range(net_node_number + 1, net_node_number + number_of_sinker + 1)])
smesh.SetName(topnodes, 'topnodes')

# define the nodes on bottom ring
bottomnodes = Mesh_1.CreateEmptyGroup(SMESH.NODE, 'bottomnodes')
nbAdd = bottomnodes.Add([i for i in range(NT * NN + 1, NT * (NN + 1) + 1)])
smesh.SetName(bottomnodes, 'bottomnodes')

# define the nodes for sinkers
sinkers = Mesh_1.CreateEmptyGroup(SMESH.NODE, 'sinkers')
nbAdd = sinkers.Add([i for i in range(net_node_number + weight_node_number - number_of_sinker + 1,
                                      net_node_number + weight_node_number + 1)])
smesh.SetName(sinkers, 'sinkers')

# define the nodes for central sinkers
conesinker = Mesh_1.CreateEmptyGroup(SMESH.NODE, 'conesinker')
nbAdd = conesinker.Add([net_node_number])
smesh.SetName(conesinker, 'conesinker')

# generate the name for each node to assign the hydrodynamic forces.
for i in range(1, len(point) + 1):
    node1 = Mesh_1.CreateEmptyGroup(SMESH.NODE, 'node%s' % i)
    nbAdd = node1.Add([i])
    smesh.SetName(node1, 'node%s' % i)

# GROUP_MA
# defaults names for all the twines and nodes.
twines = Mesh_1.CreateEmptyGroup(SMESH.EDGE, 'twines')
nbAdd = twines.AddFrom(Mesh_1.GetMesh())
smesh.SetName(twines, 'twines')

# # the top ring to keep ths shape of the fish cage.
# topring = Mesh_1.CreateEmptyGroup(SMESH.EDGE, 'topring')
# nbAdd = topring.Add([i for i in range(2, NT * (2 * NN + 1), 2 * NN + 1)])
# smesh.SetName(topring, 'topring')
#
# # bottom ring will keep the cage and add the sink forces
# bottomring = Mesh_1.CreateEmptyGroup(SMESH.EDGE, 'bottomring')
# nbAdd = bottomring.Add([i for i in range(2 * NN + 1, (NT + 1) * (2 * NN + 1), 2 * NN + 1)])
# smesh.SetName(bottomring, 'bottomring')

# give a name to the mesh
meshname = "single_cage_" + str(sys.argv[1]).split('.')[0] + ".med"
Mesh_1.ExportMED(cwd + "/" + meshname)

meshinfo = {
    "horizontalElementLength": float(pi * cage_diameter / float(NT)),
    "verticalElementLength": float(cage_height / float(NN)),
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
