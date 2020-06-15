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
mcon1 = []  # lines on mooring
mcon2 = []  # lines on weight lines
cwd = os.getcwd()

with open(str(sys.argv[1]), 'r') as f:
    content = f.read()
    cageInfo = ast.literal_eval(content)

NT = cageInfo['CageShape']['elementOverCir']  # Number of the nodes in circumference
NN = cageInfo['CageShape']['elementOverHeight']  # number of section in the height, thus, the nodes should be NN+1
BN = cageInfo['CageShape']['elementOverCone']  # number of section along the cone, thus, the nodes should be NN+1
water_depth = cageInfo['Environment']['waterDepth']  # number of section along the cone, thus, the nodes should be NN+1
cage_diameter = cageInfo['CageShape']['cageDiameter']
cage_height = cageInfo['CageShape']['cageHeight']
cage_cone_height = cageInfo['CageShape']['cageConeHeight']
cage_array = str(cageInfo['Mooring']['cageArray'])
length_of_frame_line = float(cageInfo['Mooring']['frameLineLength'])
length_of_mooring_line = float(cageInfo['Mooring']['mooringLineLength'])
length_of_bouncy_line = float(cageInfo['Mooring']['bouncyLine'])

number_of_cage_X = int(cage_array.split("-")[0])
number_of_cage_Y = int(cage_array.split("-")[1])
mooringLines = {}
nodesInMooring = []
print("The number of cages in X direction are " + str(number_of_cage_X))
print("The number of cages in X direction are " + str(number_of_cage_X))

# generate the key points of frame
point_on_frame = np.zeros((number_of_cage_X + 1, number_of_cage_Y + 1, 3))
for x in range(number_of_cage_X + 1):
    for y in range(number_of_cage_Y + 1):
        point_on_frame[x][y] = [-length_of_frame_line / 2 * number_of_cage_X + x * length_of_frame_line,
                                -length_of_frame_line / 2 * number_of_cage_Y + y * length_of_frame_line, -water_depth]
        nodesInMooring.append(point_on_frame[x][y])


point_on_buoy = np.zeros((number_of_cage_X + 1, number_of_cage_Y + 1, 3))
for x in range(number_of_cage_X + 1):
    for y in range(number_of_cage_Y + 1):
        point_on_buoy[x][y] = [-length_of_frame_line / 2 * number_of_cage_X + x * length_of_frame_line,
                               -length_of_frame_line / 2 * number_of_cage_Y + y * length_of_frame_line, 0]





print("the key points on frame are" + str(point_on_frame))



point_on_anchor = np.zeros(((number_of_cage_X + 1+number_of_cage_Y + 1)*2, 3))



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
for each_node in nodesInMooring:
    print([float(each_node[0]), float(each_node[1]), float(each_node[2])])
    nodeID = Mesh_1.AddNode(float(each_node[0]), float(each_node[1]), float(each_node[2]))
# >>>>>>>>>>







isDone = Mesh_1.Compute()

# naming  the group
# naming the node
# GROUP_NO
allnodes = Mesh_1.CreateEmptyGroup(SMESH.NODE, 'allnodes')
nbAdd = allnodes.AddFrom(Mesh_1.GetMesh())
smesh.SetName(allnodes, 'allnodes')

# generate the name for each node to assign the hydrodynamic forces.
for i in range(1, len(nodesInMooring) + 1):
    node1 = Mesh_1.CreateEmptyGroup(SMESH.NODE, 'node%s' % i)
    nbAdd = node1.Add([i])
    smesh.SetName(node1, 'node%s' % i)





meshname = "single_cage_" + str(sys.argv[1]).split('.')[0] + ".med"
Mesh_1.ExportMED(cwd + "/" + meshname)

meshinfo = {
    "horizontalElementLength": float(pi * cage_diameter / float(NT)),
    "verticalElementLength": float(cage_height / float(NN)),
    "numberOfNodes": len(point),
    "numberOfLines": len(con),
    "numberOfSurfaces": len(sur),
    "netLines": con,
    "netSurfaces": sur,
    "netNodes": point,
    "keynodes_on_frame": point_on_frame.tolist(),
    "NN": NN,
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
