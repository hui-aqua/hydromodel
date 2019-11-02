#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
based on the extral csv files

email hui.cheng@uis.no for mmore information
'''
nokey = input(
    "Please make sure you have prepared the nodes and elements files, and keep them in the same folder of creatmesh.py")

import numpy as np
import salome

salome.salome_init()
theStudy = salome.myStudy
import SMESH, SALOMEDS
from salome.smesh import smeshBuilder

smesh = smeshBuilder.New(theStudy)
Mesh_1 = smesh.Mesh()

import csv

# import the node coordinations and generate the nodes
totalnodenumber = 0
cwd = "/home/hui/aster/trawlnet/tes1trawl"

# change the path of the input file
with open(cwd + "/Nodes.csv", "r") as f:
    kk = csv.reader(f)
    i = 1
    for p in kk:
        nodeID = Mesh_1.AddNode(float(p[0]), float(p[1]), float(p[2]))
        totalnodenumber += 1

# import the line elements connection file and generate the lines
totallinenumber = 0
con = []
with open(cwd + "/Nele.csv", "r") as f:
    kk = csv.reader(f)
    i = 1
    for pp in kk:
        print(int(pp[1]), int(pp[2]))
        edge = Mesh_1.AddEdge([int(pp[1]), int(pp[2])])
        con.append([float(pp[1]) - 1, float(pp[2])] - 1)
        totallinenumber += 1

np.savetxt(cwd + '/lineconnections.txt', con)

isDone = Mesh_1.Compute()

# set group number
# defaults nname for all the twines and nodes.
twines = Mesh_1.CreateEmptyGroup(SMESH.EDGE, 'twines')
nbAdd = twines.AddFrom(Mesh_1.GetMesh())
smesh.SetName(twines, 'twines')

allnodes = Mesh_1.CreateEmptyGroup(SMESH.NODE, 'allnodes')
nbAdd = allnodes.AddFrom(Mesh_1.GetMesh())
smesh.SetName(allnodes, 'allnodes')

# define the fixed points.
fixed = Mesh_1.CreateEmptyGroup(SMESH.NODE, 'fixed')
nbAdd = fixed.Add([2711, 2712])
smesh.SetName(fixed, 'fixed')

# define the buoyancy points
buos = Mesh_1.CreateEmptyGroup(SMESH.NODE, 'buos')
nbAdd = buos.Add([
    1, 3, 6, 10, 17, 24, 33, 44, 57, 297, 298, 115, 104, 95, 88, 81, 77, 74,
    72, 71
])
smesh.SetName(buos, 'buos')

# define the sinker points
sinks = Mesh_1.CreateEmptyGroup(SMESH.NODE, 'sinks')
nbAdd = sinks.Add([
    141, 143, 146, 150, 157, 164, 173, 184, 197, 329, 330, 255, 244, 235, 228,
    221, 217, 214, 212, 211
])
smesh.SetName(sinks, 'sinks')

# generate the name for each node to assign the hycxrodynamic forces.
for i in range(1, totalnodenumber):
    node1 = Mesh_1.CreateEmptyGroup(SMESH.NODE, 'node%s' % i)
    nbAdd = node1.Add([i])
    smesh.SetName(node1, 'node%s' % i)
