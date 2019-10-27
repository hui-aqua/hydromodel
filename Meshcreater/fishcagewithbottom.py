"""
The center of the floating collar is (0,0,0)
Fish cage is along the Z- direction
Z=0 is the free surface
Z<0 is the water zone
Z>0 is the air zone
The fish cage is a cylindrical shape
The fish cage has a bottom, and the bottom can be flat or cone shape
 (according to the "cagebottomcenter" at line 37)

Because it is dependent on individual cage.
This code can be executed by the following command in terminal:

/opt/salome2019/appli_V2019_univ/salome -t ~/GitCode/aqua/hydromodel/Meshcreater/fishcagewithbottom.py

or:

/opt/salome2019/appli_V2019_univ/salome -t fishcagewithbottom.py

Any questions about this code, please email: hui.cheng@uis.no

"""
import os

# define the fish cage shape
import numpy as np
from numpy import pi

D = 50.0  # [m]  fish cage diameter
H = 30.0  # [m]  fish cage height
# L = 1.5  # [m]  bar length
NT = 30  # it can use int(pi*D/L)   # Number of the nodes in circumference
# NT = int(pi * D / L)
NN = 20  # it can use int(H/L)      # number of section in the height, thus, the nodes should be NN+1
# NN = int(H / L)
p = []
cagebottomcenter = [0, 0, -H]

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


con = []
sur = []
for i in range(1, NT + 1):  # todo check con and sur
    for j in range(0, NN + 1):
        if j == NN:
            edge = Mesh_1.AddEdge([i + j * NT, len(p)])  # add the vertical line into geometry
            con.append([i + j * NT - 1, len(p) - 1])  # add the vertical line into geometry
            if i == NT:
                edge = Mesh_1.AddEdge([i + j * NT, 1 + i + (j - 1) * NT])  # add the horizontal line into geometry
                con.append([i + j * NT - 1, 1 + i + (j - 1) * NT - 1])  # add the horizontal line into geometry
                sur.append([i + j * NT - 1, 1 + i + (j - 1) * NT - 1, len(p) - 1, len(p) - 1])
            else:
                edge = Mesh_1.AddEdge([i + j * NT, 1 + i + j * NT])  # add the horizontal line into geometry
                con.append([i + j * NT - 1, 1 + i + j * NT - 1])  # add the horizontal line into geometry
                sur.append([i + j * NT - 1, 1 + i + j * NT - 1, len(p) - 1, len(p) - 1])
        else:
            edge = Mesh_1.AddEdge([i + j * NT, i + (j + 1) * NT])  # add the vertical line into geometry
            con.append([i + j * NT - 1, i + (j + 1) * NT - 1])  # add the vertical line into geometry
            if i == NT:
                edge = Mesh_1.AddEdge([i + j * NT, 1 + i + (j - 1) * NT])  # add the horizontal line into geometry
                con.append([i + j * NT - 1, 1 + i + (j - 1) * NT - 1])  # add the horizontal line into geometry
                sur.append([i + j * NT - 1, 1 + i + (j - 1) * NT - 1, i + j * NT - 1, i + (j + 1) * NT - 1])
            else:
                edge = Mesh_1.AddEdge([i + j * NT, 1 + i + j * NT])  # add the horizontal line into geometry
                con.append([i + j * NT - 1, 1 + i + j * NT - 1])  # add the horizontal line into geometry
                sur.append([i + j * NT - 1, 1 + i + j * NT - 1, len(p) - 1, len(p) - 1])


cwd = "/home/hui/GitCode/aqua/hydromodel"
cwd = os.getcwd()
np.savetxt(cwd + '/lines.txt', con)
np.savetxt(cwd + '/surfaces.txt', sur)


isDone = Mesh_1.Compute()
# nameing  the group

# defaults nname for all the twines and nodes.
twines = Mesh_1.CreateEmptyGroup(SMESH.EDGE, 'twines')
nbAdd = twines.AddFrom(Mesh_1.GetMesh())
smesh.SetName(twines, 'twines')

allnodes = Mesh_1.CreateEmptyGroup(SMESH.NODE, 'allnodes')
nbAdd = allnodes.AddFrom(Mesh_1.GetMesh())
smesh.SetName(allnodes, 'allnodes')
# todo check the nameing process
# define the fixed points, the reaction forces are calculated based on fixed points.
fixed = Mesh_1.CreateEmptyGroup(SMESH.NODE, 'fixed')
nbAdd = fixed.Add([i for i in range(NT + 1)])
smesh.SetName(fixed, 'fixed')

# bottom ring will keep the cage and add the sink forces
bottomring = Mesh_1.CreateEmptyGroup(SMESH.EDGE, 'bottomring')
nbAdd = bottomring.Add([i for i in range(1 + NN, 1 + (NT) * (NN + 1), NN + 1)])
smesh.SetName(bottomring, 'bottomring')

# the top ring to keep ths shape of the fish cage.
topring = Mesh_1.CreateEmptyGroup(SMESH.EDGE, 'topring')
nbAdd = topring.Add([i for i in range(1, 1 + (NT) * (NN + 1), NN + 1)])
smesh.SetName(topring, 'topring')

# generate the name for each node to assign the hycxrodynamic forces.
for i in range(1, (NN + 1) * NT + 1):
    node1 = Mesh_1.CreateEmptyGroup(SMESH.NODE, 'node%s' % i)
    nbAdd = node1.Add([i])
    smesh.SetName(node1, 'node%s' % i)

Mesh_1.ExportMED(cwd + "/MyMesh.med")
