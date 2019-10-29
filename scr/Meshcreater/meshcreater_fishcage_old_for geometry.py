#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
The center of the floating collar is (0,0,0)
Fish cage is along the Z direction

1. open Salome_meca
2. select "geomery" --> load script (this one)
3. select all the lines and fuse them. (it will take a while if too many lines)
4. switch to mesh and creat mesh
5. use 1D-->wire discretisation-->local length--> a little larger than the "L" in this script
6. Creat group name and node name to be used in code_Aster
    6.1 essiential name: allnodes twines
7. Export to med file
8. 

'''
import numpy as np
from numpy import pi
import salome
from salome.geom import geomBuilder
salome.salome_init()
geompy = geomBuilder.New(salome.myStudy)
gg = salome.ImportComponentGUI("GEOM")

Point = [None] * (500000)  # initinal 300 points
Line = [None] * (600000)  # initial 600 line
# the above should be large enough.
D = 50  # [m]  fish cage diameter
H = 30  # [m]  fish cage height
L = 3  # [m]  bar length
NT = 50  # it can use int(pi*D/L)   # Number of the meshes in circumference
NN = 10  # it can use int(H/L)      # Number of the meshes in the height
p = np.zeros([(NN + 1) * NT, 3])
# generate the point coordinates matrix
for i in range(0, NT):
    for j in range(0, NN + 1):
        p[i + j * NT, :] = [
            D / 2 * np.cos(i * 2 * pi / NT), D / 2 * np.sin(i * 2 * pi / NT),
            -j * L
        ]

# add the points into geometry
for i in range(0, len(p)):
    Point[i] = geompy.MakeVertex(p[i, 0], p[i, 1], p[i, 2])
    geompy.addToStudy(Point[i], "P_" + str(i))

# add the horizontial line into geometry
for i in range(0, NT):
    for j in range(0, NN + 1):
        if i == NT - 1:
            Line[i + j * NT] = geompy.MakeLineTwoPnt(Point[i + j * NT],
                                                     Point[j * NT])
            geompy.addToStudy(Line[i + j * NT], "L_" + str(i + j * NT))
        else:
            Line[i + j * NT] = geompy.MakeLineTwoPnt(Point[i + j * NT],
                                                     Point[1 + i + j * NT])
            geompy.addToStudy(Line[i + j * NT], "L_" + str(i + j * NT))
# add the vertical line into geometry
for i in range(0, NT):
    for j in range(0, NN):
        Line[(NN + 1) * NT + i + j * NT] = geompy.MakeLineTwoPnt(
            Point[i + j * NT], Point[i + (j + 1) * NT])
        geompy.addToStudy(Line[(NN + 1) * NT + i + j * NT],
                          "L_" + str((1 + NN) * NT + i + j * NT))

if salome.sg.hasDesktop():
    salome.sg.updateObjBrowser(1)
