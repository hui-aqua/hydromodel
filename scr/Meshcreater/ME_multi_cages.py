"""
The center of the floating collar is (0,0,0)
Fish cage is along the Z- direction
Z=0 is the free surface
Z<0 is the water zone
Z>0 is the air zone
The fish cage is a cylindrical shape
The fish cage has no bottom net
The weight system for the fish cage only has sinkers


Any questions about this code, please email: hui.cheng@uis.no

"""
import sys
import os
import numpy as np
from numpy import pi
import ast

point = []
con = []
sur = []
cwd = os.getcwd()

with open(str(sys.argv[1]), 'r') as f:
    content = f.read()
    cageInfo = ast.literal_eval(content)

D = cageInfo['CageShape']['cageDiameter']
H = cageInfo['CageShape']['cageHeight']
NT = cageInfo['CageShape']['elementOverCir']  # Number of the nodes in circumference
NN = cageInfo['CageShape']['elementOverHeight']  # number of section in the height, thus, the nodes should be NN+1

num_cages = int(np.array(cageInfo['FloatingCollar']['floaterCenter']).size / 3)
floatingCenter = cageInfo['FloatingCollar']['floaterCenter']
print("Number of cages are  " + str(num_cages))

# generate the point coordinates matrix for the net
Num_nodesInOneCage = NT * (NN + 1)

# the below is the commond in the Mesh, Salome.
# the mesh creater script
for cageI in range(num_cages):
    print("Creating cage  " + str(cageI))
    for j in range(0, NN + 1):
        for i in range(0, NT):
            point.append([floatingCenter[cageI][0] + D / 2 * np.cos(i * 2 * pi / float(NT)),
                          floatingCenter[cageI][1] + D / 2 * np.sin(i * 2 * pi / float(NT)),
                          floatingCenter[cageI][2] - j * H / float(NN)])

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

for cageI in range(num_cages):
    for i in range(1, NT + 1):
        for j in range(0, NN + 1):
            if j == NN:
                if i == NT:
                    edge = Mesh_1.AddEdge([i + j * NT + Num_nodesInOneCage * cageI,
                                           1 + i + (j - 1) * NT + Num_nodesInOneCage * cageI])  # add the horizontal line into geometry
                    con.append([i + j * NT - 1 + Num_nodesInOneCage * cageI,
                                1 + i + (j - 1) * NT - 1 + Num_nodesInOneCage * cageI])   # add the horizontal line into con
                else:
                    edge = Mesh_1.AddEdge([i + j * NT + Num_nodesInOneCage * cageI,
                                           1 + i + j * NT + Num_nodesInOneCage * cageI])  # add the horizontal line into geometry
                    con.append([i + j * NT - 1 + Num_nodesInOneCage * cageI,
                                1 + i + j * NT - 1 + Num_nodesInOneCage * cageI])        # add the horizontal line into con
            else:
                edge = Mesh_1.AddEdge([i + j * NT + Num_nodesInOneCage * cageI,
                                       i + (j + 1) * NT + Num_nodesInOneCage * cageI])  # add the vertical line into geometry
                con.append([i + j * NT - 1 + Num_nodesInOneCage * cageI,
                            i + (j + 1) * NT - 1 + Num_nodesInOneCage * cageI])  # add the vertical line into con
                if i == NT:
                    edge = Mesh_1.AddEdge([i + j * NT + Num_nodesInOneCage * cageI,
                                           1 + i + (j - 1) * NT + Num_nodesInOneCage * cageI])  # add the horizontal line into geometry
                    con.append([i + j * NT - 1 + Num_nodesInOneCage * cageI,
                                1 + i + (j - 1) * NT - 1 + Num_nodesInOneCage * cageI])  # add the horizontal line into con
                    sur.append([i + j * NT - 1 + Num_nodesInOneCage * cageI,
                                1 + i + (j - 1) * NT - 1 + Num_nodesInOneCage * cageI,
                                i + (j + 1) * NT - 1 + Num_nodesInOneCage * cageI,
                                1 + i + j * NT - 1 + Num_nodesInOneCage * cageI])
                # add the horizontal surface into sur
                else:
                    edge = Mesh_1.AddEdge([i + j * NT + Num_nodesInOneCage * cageI,
                                           1 + i + j * NT + Num_nodesInOneCage * cageI])  # add the horizontal line into geometry
                    con.append([i + j * NT - 1 + Num_nodesInOneCage * cageI,
                                1 + i + j * NT - 1 + Num_nodesInOneCage * cageI])  # add the horizontal line into con
                    sur.append([i + j * NT - 1 + Num_nodesInOneCage * cageI,
                                1 + i + j * NT - 1 + Num_nodesInOneCage * cageI,
                                i + (j + 1) * NT - 1 + Num_nodesInOneCage * cageI,
                                1 + i + (j + 1) * NT - 1 + Num_nodesInOneCage * cageI])
                # add the horizontal surface into sur

isDone = Mesh_1.Compute()
# naming  the group
# GROUP_NO
allnodes = Mesh_1.CreateEmptyGroup(SMESH.NODE, 'allnodes')
nbAdd = allnodes.AddFrom(Mesh_1.GetMesh())
smesh.SetName(allnodes, 'allnodes')

# define the topnodes, the reaction forces are calculated based on topnodes.
topnodeid = []
for pID in point:
    if pID[2] == floatingCenter[0][2]:
        topnodeid.append(point.index(pID) + 1)
topnodes = Mesh_1.CreateEmptyGroup(SMESH.NODE, 'topnodes')
nbAdd = topnodes.Add(topnodeid)
smesh.SetName(topnodes, 'topnodes')

# define the nodes on bottom ring
bottomNodeId = []
for pID in point:
    if pID[2] == floatingCenter[0][2]-H:
        bottomNodeId.append(point.index(pID) + 1)
bottomnodes = Mesh_1.CreateEmptyGroup(SMESH.NODE, 'bottomnodes')
nbAdd = bottomnodes.Add(bottomNodeId)
smesh.SetName(bottomnodes, 'bottomnodes')

# define the nodes for sinkers
sinkers = Mesh_1.CreateEmptyGroup(SMESH.NODE, 'sinkers')
if cageInfo['Weight']['weightType'] in 'sinkers':
    NS = float(cageInfo['Weight']['numOfSinkers'])
    if (float(cageInfo['CageShape']['elementOverCir']) / NS).is_integer():
        print("The sinkers are evenly distributed in the bottom.")
        sinkerNodeId = []
        for cageI in range(num_cages):
            sinkerNodeId = [i for i in
                            range(len(point) - NT + 1 - Num_nodesInOneCage * cageI,
                                  len(point) - Num_nodesInOneCage * cageI,
                                  int(cageInfo['CageShape']['elementOverCir'] / NS))]
            nbAdd = sinkers.Add(sinkerNodeId)
        smesh.SetName(sinkers, 'sinkers')
    else:
        print("The sinkers can not be evenly distributed in the bottom.")
else:
    print("There is no sinkers on the bottom ring")


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

# the top ring to keep ths shape of the fish cage.
top_element=[]
for i in range(2, len(con) + 1, 2 * NN + 1):
    top_element.append(i)
topring = Mesh_1.CreateEmptyGroup(SMESH.EDGE, 'topring')
nbAdd = topring.Add(top_element)
smesh.SetName(topring, 'topring')
#
#
# # bottom ring will keep the cage and add the sink forces
bottom_element=[]
for i in range(2 * NN + 1, len(con) + 1, 2 * NN + 1):
    bottom_element.append(i)
bottomring = Mesh_1.CreateEmptyGroup(SMESH.EDGE, 'bottomring')
nbAdd = bottomring.Add(bottom_element)
smesh.SetName(bottomring, 'bottomring')


meshname = "Threecage" + str(D) + "X" + str(H) + ".med"
Mesh_1.ExportMED(cwd + "/" + meshname)

meshinfo = {
    "horizontalElementLength": float(pi * D / NT),
    "verticalElementLength": float(H / NN),
    "numberOfNodes": len(point),
    "numberOfLines": len(con),
    "numberOfSurfaces": len(sur),
    "netLines": con,
    "netSurfaces": sur,
    "netNodes": point,
    "NN": NN,
    "NT": NT,
    "meshName": meshname,
    "numberOfCages": num_cages,
}
f = open(cwd + "/meshinfomation.txt", "w")
f.write(str(meshinfo))
f.close()
