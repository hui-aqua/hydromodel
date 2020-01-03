"""
The center of the floating collar is (0,0,0)
Fish cage is along the Z- direction
Z=0 is the free surface
Z<0 is the water zone
Z>0 is the air zone
The fish cage is a cylindrical shape
The fish cage has a bottom, and the bottom can be flat or cone shape
 (according to the "cagebottomcenter" at line 37)
The weight system for the fish cage only have sinker tube and center weight.
Because it is dependent on individual cage.
Any questions about this code, please email: hui.cheng@uis.no

"""
import sys
import os
import numpy as np
from numpy import pi

cwd = os.getcwd()
Dictname = str(sys.argv[1])

with open(Dictname, 'r') as f:
    content = f.read()
    cageinfo = eval(content)

D = cageinfo['CageShape']['cageDiameter']
H = cageinfo['CageShape']['cageHeight']
NT = cageinfo['CageShape']['elementOverCir']  # Number of the nodes in circumference
NN = cageinfo['CageShape']['elementOverHeight']  # number of section in the height, thus, the nodes should be NN+1
Dtip = cageinfo['CageShape']['cageCenterTip']
cagebottomcenter = [0, 0, -Dtip]

p = []
con = []
sur = []

# generate the point coordinates matrix for the net
for j in range(0, NN + 1):
    for i in range(0, NT):
        p.append([D / 2 * np.cos(i * 2 * pi / float(NT)), D / 2 * np.sin(i * 2 * pi / float(NT)), -j * H / float(NN)])
p.append(cagebottomcenter)

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
for i in range(len(p)):
    nodeID = Mesh_1.AddNode(float(p[i][0]), float(p[i][1]), float(p[i][2]))

for i in range(1, NT + 1):
    for j in range(0, NN + 1):
        if j == NN:
            edge = Mesh_1.AddEdge([i + j * NT, len(p)])  # add the vertical line into geometry
            con.append([i + j * NT - 1, len(p) - 1])  # add the vertical line into geometry
            if i == NT:
                edge = Mesh_1.AddEdge([i + j * NT, 1 + i + (j - 1) * NT])  # add the horizontal line into geometry
                con.append([(j + 1) * NT - 1, j * NT])  # add the horizontal line into geometry
                sur.append([(j + 1) * NT - 1, j * NT, (j + 1) * NT - 2, len(p) - 1])
                # add the cone surface into sur
            else:
                edge = Mesh_1.AddEdge([i + j * NT, 1 + i + j * NT])  # add the horizontal line into geometry
                con.append([i + j * NT - 1,
                            i + j * NT])  # add the horizontal line into geometry
                if i * 2 + j * NT < len(p) - 1:
                    sur.append([i * 2 + j * NT - 2, i * 2 + j * NT - 1, i * 2 + j * NT, len(p) - 1])
                # add the cone surface into sur
        else:
            edge = Mesh_1.AddEdge([i + j * NT, i + (j + 1) * NT])  # add the vertical line into geometry
            con.append([i + j * NT - 1, i + (j + 1) * NT - 1])  # add the vertical line into geometry
            if i == NT:
                edge = Mesh_1.AddEdge([i + j * NT, 1 + i + (j - 1) * NT])  # add the horizontal line into geometry
                con.append([i + j * NT - 1, 1 + i + (j - 1) * NT - 1])  # add the horizontal line into geometry
                sur.append([i + j * NT - 1, 1 + i + (j - 1) * NT - 1, i + (j + 1) * NT - 1, 1 + i + j * NT - 1])
                # add the horizontal surface into sur
            else:
                edge = Mesh_1.AddEdge([i + j * NT, 1 + i + j * NT])  # add the horizontal line into geometry
                con.append([i + j * NT - 1, 1 + i + j * NT - 1])  # add the horizontal line into geometry
                sur.append([i + j * NT - 1, 1 + i + j * NT - 1, i + (j + 1) * NT - 1, 1 + i + (j + 1) * NT - 1])
                # add the horizontal surface into sur


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

# define the node on the bottom tip
bottomtip = Mesh_1.CreateEmptyGroup(SMESH.NODE, 'bottomtip')
nbAdd = bottomtip.Add([len(p)])
smesh.SetName(bottomtip, 'bottomtip')

# generate the name for each node to assign the hycxrodynamic forces.
for i in range(1, len(p) + 1):
    node1 = Mesh_1.CreateEmptyGroup(SMESH.NODE, 'node%s' % i)
    nbAdd = node1.Add([i])
    smesh.SetName(node1, 'node%s' % i)

# GROUP_MA
# defaults names for all the twines and nodes.
twines = Mesh_1.CreateEmptyGroup(SMESH.EDGE, 'twines')
nbAdd = twines.AddFrom(Mesh_1.GetMesh())
smesh.SetName(twines, 'twines')

# the top ring to keep ths shape of the fish cage.
topring = Mesh_1.CreateEmptyGroup(SMESH.EDGE, 'topring')
nbAdd = topring.Add([i for i in range(2, len(con) + 1, 2 * NN + 2)])
smesh.SetName(topring, 'topring')

# bottom ring will keep the cage and add the sink forces
bottomring = Mesh_1.CreateEmptyGroup(SMESH.EDGE, 'bottomring')
nbAdd = bottomring.Add([i for i in range(2 * (1 + NN), len(con) + 1, 2 * (NN + 1))])
smesh.SetName(bottomring, 'bottomring')

meshname = "CFGWB" + str(D) + "X" + str(H) + ".med"
Mesh_1.ExportMED(cwd + "/" + meshname)

meshinfo = {
    "horizontalElementLength": float(pi * D / NT),
    "verticalElementLength": float(H / NN),
    "numberOfNodes": len(p),
    "numberOfLines": len(con),
    "numberOfSurfaces": len(sur),
    "netLines": con,
    "netSurfaces": sur,
    "netNodes": p,
    "NN": NN,
    "NT": NT,
    "meshName": meshname
}
f = open(cwd + "/meshinfomation.txt", "w")
f.write(str(meshinfo))
f.close()
