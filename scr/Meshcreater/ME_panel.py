"""
----------------------------------
--   University of Stavanger    --
--           Hui Cheng          --
----------------------------------
Any questions about this code,
please email: hui.cheng@uis.no

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

NT = cageInfo['Net']['meshOverWidth']  # Number of the nodes in circumference
NN = cageInfo['Net']['meshOverHeight']  # number of section in the height, thus, the nodes should be NN+1
net_width = cageInfo['Net']['netWidth']
net_height = cageInfo['Net']['netHeight']
top_center = cageInfo['TopBar']['barCenter']
nettingType = cageInfo['Net']['nettingType']
normal_vector = cageInfo['Net']['normalVector']  # todo add the linear transformation matrix later

# generate the point coordinates matrix for a net panel
if nettingType == "square":
    for net in top_center:
        for j in range(0, NN + 1):
            for i in range(0, NT + 1):
                point.append(
                    [net[0],
                     net[1] - net_width / 2 + (i / float(NT) * net_width),
                     net[2] - j / float(NN) * net_height])
    nodes_on_eachNet = (NN + 1) * (NT + 1)
    elements_on_eachNet = (NN + 1) * NT + NN * (NT + 1)

elif nettingType == "rhombus":
    print("Under construction")
    exit()  # todo add the rhombus nodes.
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
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> salome

# add the pints into geometry
for each_node in point:
    nodeID = Mesh_1.AddNode(float(each_node[0]), float(each_node[1]), float(each_node[2]))
#

for k in range(len(top_center)):
    for i in range(0, NT + 1):
        for j in range(0, NN + 1):
            if j != NN:
                edge = Mesh_1.AddEdge(
                    [nodes_on_eachNet * k + 1 + i + j * (NT + 1),
                     nodes_on_eachNet * k + 1 + i + (j + 1) * (NT + 1)])  # add the vertical line into geometry
                con.append([nodes_on_eachNet * k + i + j * (NT + 1),
                            nodes_on_eachNet * k + i + (j + 1) * (NT + 1)])  # add the vertical line into con
            if i != NT:
                edge = Mesh_1.AddEdge(
                    [nodes_on_eachNet * k + 1 + i + j * (NT + 1),
                     nodes_on_eachNet * k + 1 + 1 + i + j * (NT + 1)])  # add the horizontal line into geometry
                con.append([nodes_on_eachNet * k + i + j * (NT + 1),
                            nodes_on_eachNet * k + 1 + i + j * (NT + 1)])  # add the horizontal line into con
            if i != NT and j != NN:
                sur.append([nodes_on_eachNet * k + i + j * (NT + 1),
                            nodes_on_eachNet * k + 1 + i + j * (NT + 1),
                            nodes_on_eachNet * k + i + (j + 1) * (NT + 1),
                            nodes_on_eachNet * k + 1 + i + (j + 1) * (NT + 1)])

isDone = Mesh_1.Compute()
# naming  the group
# GROUP_NO
allnodes = Mesh_1.CreateEmptyGroup(SMESH.NODE, 'allnodes')
nbAdd = allnodes.AddFrom(Mesh_1.GetMesh())
smesh.SetName(allnodes, 'allnodes')

# define the top nodes
topnodes = Mesh_1.CreateEmptyGroup(SMESH.NODE, 'topnodes')
for k in range(len(top_center)):
    nbAdd = topnodes.Add([i for i in range(k * nodes_on_eachNet + 1, k * nodes_on_eachNet + NT + 2)])
smesh.SetName(topnodes, 'topnodes')

# define the nodes on bottom ring
bottomnodes = Mesh_1.CreateEmptyGroup(SMESH.NODE, 'bottomnodes')
for k in range(len(top_center)):
    nbAdd = bottomnodes.Add(
        [i for i in range(k * nodes_on_eachNet + (NN) * (NT + 1) + 1, k * nodes_on_eachNet + (NN + 1) * (NT + 1) + 1)])
smesh.SetName(bottomnodes, 'bottomnodes')

# define the nodes for sinkers
if cageInfo['Weight']['weightType'] in ['sinkers']:
    print("\n\n\n------------------>> Note:"
          "\nYou need to add the sinker manually.\n"
          "Name the sinkers in salome_meca.\n\n\n")

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
#
# # the top ring to keep ths shape of the fish cage.
topring = Mesh_1.CreateEmptyGroup(SMESH.EDGE, 'topring')
for k in range(len(top_center)):
    nbAdd = topring.Add(
        [i for i in range(k * elements_on_eachNet + 2, k * elements_on_eachNet + NT * (2 * NN + 1), 2 * NN + 1)])
smesh.SetName(topring, 'topring')

# bottom ring will keep the cage and add the sink forces
bottomring = Mesh_1.CreateEmptyGroup(SMESH.EDGE, 'bottomring')
for k in range(len(top_center)):
    nbAdd = bottomring.Add([i for i in range(k * elements_on_eachNet + 2 * NN + 1,
                                             k * elements_on_eachNet + (NT + 1) * (2 * NN + 1), 2 * NN + 1)])
smesh.SetName(bottomring, 'bottomring')

# # give a name to the mesh
meshname = "NetPanel_" + str(sys.argv[1]).split('.')[0] + ".med"
Mesh_1.ExportMED(cwd + "/" + meshname)

meshinfo = {
    "horizontalElementLength": float(net_width / NT),
    "verticalElementLength": float(net_height / NN),
    "numberOfNodes": len(point),
    "numberOfLines": len(con),
    "numberOfSurfaces": len(sur),
    "netLines": con,
    "netSurfaces": sur,
    "netNodes": point,
    "NN": NN,
    "NT": NT,
    "meshName": meshname
}
print("\n"
      "  ----------------------------------\n"
      "  --   University of Stavanger    --\n"
      "  --           Hui Cheng          --\n"
      "  ----------------------------------\n"
      "  Any questions about this code,\n"
      "  please email: hui.cheng@uis.no\n"
      "  Net panel(s)")
print("<<<<<<<<<< Mesh Information >>>>>>>>>>")
print("Number of node is " + str(meshinfo["numberOfNodes"]) + ".")
print("Number of line element is " + str(meshinfo["numberOfLines"]) + ".")
print("Number of surface element is " + str(meshinfo["numberOfSurfaces"]) + ".\n")
with open(cwd + "/meshinfomation.py", 'w') as f:
    f.write("meshinfo=")
    f.write(str(meshinfo))
f.close()
