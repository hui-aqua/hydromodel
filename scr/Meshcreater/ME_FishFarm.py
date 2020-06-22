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

cwd = os.getcwd()

with open(str(sys.argv[1]), 'r') as f:
    content = f.read()
    cageInfo = ast.literal_eval(content)

water_depth = cageInfo['Environment']['waterDepth']  # number of section along the cone, thus, the nodes should be NN+1
NT = cageInfo['CageShape']['elementOverCir']  # Number of the nodes in circumference
NN = cageInfo['CageShape']['elementOverHeight']  # number of section in the height, thus, the nodes should be NN+1
BN = cageInfo['CageShape']['elementOverCone']  # number of section along the cone, thus, the nodes should be NN+1

cage_height = cageInfo['CageShape']['cageHeight']
cage_cone_height = cageInfo['CageShape']['cageConeHeight']
netpen_diameter = cageInfo['CageShape']['cageDiameter']

floating_diameter = cageInfo['FloatingCollar']['diameter']
sinktube_depth = cageInfo['Weight']['pipeDepth']

cage_array = str(cageInfo['Mooring']['cageArray'])
length_of_frame_line = float(cageInfo['Mooring']['frameLineLength'])
length_of_mooring_line = float(cageInfo['Mooring']['mooringLineLength'])
length_of_bouncy_line = float(cageInfo['Mooring']['bouncyLine'])
number_of_floating_segement = cageInfo['FloatingCollar']['elementOverCir']

number_of_cage_X = int(cage_array.split("-")[0])
number_of_cage_Y = int(cage_array.split("-")[1])
print("The number of cages in X direction are " + str(number_of_cage_X))
print("The number of cages in X direction are " + str(number_of_cage_X))

# todo fixed the naming

con_mooring = []
point_mooring = []  # points on netting

point_netting = []  # points on netting
con_netting = []  # lines on netting
sur_netting = []  # surface on netting

nodesInMooring = []
mooringLines = {}

# generate the key points of frame
key_point_buoy = np.zeros((number_of_cage_Y + 1, number_of_cage_X + 1, 3))
for y in range(number_of_cage_Y + 1):
    for x in range(number_of_cage_X + 1):
        key_point_buoy[y][x] = [-length_of_frame_line / 2 * number_of_cage_X + x * length_of_frame_line,
                                length_of_frame_line / 2 * number_of_cage_Y - y * length_of_frame_line, 0]
        nodesInMooring.append(key_point_buoy[y][x])

key_point_conjunction = np.zeros((number_of_cage_Y + 1, number_of_cage_X + 1, 3))
for y in range(number_of_cage_Y + 1):
    for x in range(number_of_cage_X + 1):
        key_point_conjunction[y][x] = key_point_buoy[y][x] - np.array([0, 0, length_of_bouncy_line])
        nodesInMooring.append(key_point_conjunction[y][x])

point_on_anchor_x = np.zeros((2, number_of_cage_X + 1, 3))
point_on_anchor_y = np.zeros((number_of_cage_Y + 1, 2, 3))
for index in range(2):
    for x in range(number_of_cage_X + 1):
        point_on_anchor_x[index, x] = key_point_buoy[-index][x] + \
                                      np.array([0, int(1 - 2 * index) * length_of_mooring_line, -water_depth])
        nodesInMooring.append(point_on_anchor_x[index, x])

for index in range(2):
    for y in range(number_of_cage_Y + 1):
        point_on_anchor_y[y, index] = key_point_buoy[y][-index] + \
                                      np.array([(2 * index - 1) * length_of_mooring_line, 0, -water_depth])
        nodesInMooring.append(point_on_anchor_y[y, index])

# k  point on floater center
center_floating = np.zeros((number_of_cage_Y, number_of_cage_X, 3))
for y in range(number_of_cage_Y):
    for x in range(number_of_cage_X):
        center_floating[y, x] = np.array([-length_of_frame_line / 2 * (number_of_cage_X - 1) + x * length_of_frame_line,
                                          length_of_frame_line / 2 * (number_of_cage_Y - 1) - y * length_of_frame_line,
                                          0])
        nodesInMooring.append(center_floating[y, x])

    # k  point on bottom ring center
center_bottomring = np.zeros((number_of_cage_Y, number_of_cage_X, 3))
for y in range(number_of_cage_Y):
    for x in range(number_of_cage_X):
        center_bottomring[y, x] = np.array(
            [-length_of_frame_line / 2 * (number_of_cage_X - 1) + x * length_of_frame_line,
             length_of_frame_line / 2 * (number_of_cage_Y - 1) - y * length_of_frame_line,
             -sinktube_depth])
        nodesInMooring.append(center_bottomring[y, x])

key_point_bridle_top = np.zeros((number_of_cage_Y, number_of_cage_X, number_of_floating_segement, 3))
for y in range(number_of_cage_Y):
    for x in range(number_of_cage_X):
        for i in range(number_of_floating_segement):
            key_point_bridle_top[y, x, i] = np.array([-length_of_frame_line / 2 * (
                    number_of_cage_X - 1) + x * length_of_frame_line + floating_diameter / 2 * np.cos(
                i * 2 * np.pi / number_of_floating_segement),
                                                      length_of_frame_line / 2 * (
                                                              number_of_cage_Y - 1) - y * length_of_frame_line + floating_diameter / 2 * np.sin(
                                                          i * 2 * np.pi / number_of_floating_segement),
                                                      0])
            nodesInMooring.append(key_point_bridle_top[y, x, i])

key_point_bridle_bottom = np.zeros((number_of_cage_Y, number_of_cage_X, number_of_floating_segement, 3))
for y in range(number_of_cage_Y):
    for x in range(number_of_cage_X):
        for i in range(number_of_floating_segement):
            key_point_bridle_bottom[y, x, i] = np.array([-length_of_frame_line / 2 * (
                    number_of_cage_X - 1) + x * length_of_frame_line + floating_diameter / 2 * np.cos(
                i * 2 * np.pi / number_of_floating_segement),
                                                         length_of_frame_line / 2 * (
                                                                 number_of_cage_Y - 1) - y * length_of_frame_line + floating_diameter / 2 * np.sin(
                                                             i * 2 * np.pi / number_of_floating_segement),
                                                         -sinktube_depth])
            nodesInMooring.append(key_point_bridle_bottom[y, x, i])


# buoylines
number_of_buoy = (number_of_cage_Y + 1) * (number_of_cage_X + 1)
for index in range(number_of_buoy):
    mooringLines["buoyLine" + str(index)] = [index, index + number_of_buoy]

# framelines
number_of_frameX = number_of_cage_X * (number_of_cage_Y + 1)
number_of_frameY = number_of_cage_Y * (number_of_cage_X + 1)

for y in range(number_of_cage_Y + 1):
    for x in range(number_of_cage_X):
        mooringLines["frameLineX" + str(y) + "_" + str(x)] = [number_of_buoy + x + (number_of_cage_X + 1) * y,
                                                              number_of_buoy + x + (number_of_cage_X + 1) * y + 1]
for y in range(number_of_cage_Y):
    for x in range(number_of_cage_X + 1):
        mooringLines["frameLineY" + str(y) + "_" + str(x)] = [number_of_buoy + x + (number_of_cage_X + 1) * y,
                                                              number_of_buoy + x + (number_of_cage_X + 1) * (y + 1)]
# anchorlines
number_of_anchor = 2 * (number_of_cage_Y + 1) + 2 * (number_of_cage_X + 1)
for index in range(number_of_cage_X + 1):
    mooringLines["anchorLine_x0_" + str(index)] = [index + 2 * number_of_buoy, index + number_of_buoy]
    mooringLines["anchorLine_x1_" + str(index)] = [number_of_cage_X + 1 + index + 2 * number_of_buoy,
                                                   index + 2 * number_of_buoy - (number_of_cage_X + 1)]

for index in range(number_of_cage_Y + 1):
    mooringLines["anchorLine_y0_" + str(index)] = [index + 2 * number_of_buoy + (number_of_cage_X + 1) * 2,
                                                   index * (number_of_cage_X + 1) + number_of_buoy]
    mooringLines["anchorLine_y1_" + str(index)] = [
        index + 2 * number_of_buoy + (number_of_cage_X + 1) * 2 + (number_of_cage_Y + 1),
        (index + 1) * (number_of_cage_X + 1) + number_of_buoy - 1]

# vertical bridles
#                    number of buoy poing and frame points     + number of anchor point
number_of_key_node1 = (number_of_cage_X + 1) * (number_of_cage_Y + 1) * 2 + 2 * (number_of_cage_X + 1) + 2 * (
        number_of_cage_Y + 1) + number_of_cage_X * number_of_cage_Y * 2
number_of_vertical_bridle = number_of_floating_segement * (number_of_cage_Y) * (number_of_cage_X)
for y in range(number_of_cage_Y):
    for x in range(number_of_cage_X):
        for i in range(number_of_floating_segement):
            mooringLines["bridlesV" + str(y) + "_" + str(x) + "_" + str(i)] = [
                number_of_key_node1 + number_of_cage_X * number_of_floating_segement * y + number_of_floating_segement * x + i,
                number_of_key_node1 + number_of_floating_segement * number_of_cage_X * number_of_cage_Y + number_of_cage_X * number_of_floating_segement * y + number_of_floating_segement * x + i]

# ! #FIXME: the conject_* list should be auto_updated according to the array of fish farm
# horizontal bridles

number_of_horizontal_bridle = 12 * number_of_cage_Y * number_of_cage_X

if number_of_cage_X == 1 and number_of_cage_Y == 1:
    conject_plate = [5, 4, 6, 7]
    conject_floating = [19, 20, 21, 23, 24, 25, 27, 28, 29, 31, 32, 33]
    for i in range(12):
        mooringLines["bridlesH" + str(y) + "_" + str(x) + "_" + str(i)] = [conject_plate[int(i / 3)],
                                                                           conject_floating[i]]
elif number_of_cage_X == 4 and number_of_cage_Y == 1:
    conject_plate = [11, 10, 15, 16, 12, 11, 16, 17, 13, 12, 17, 18, 14, 13, 18, 19]
    conject_floating = [43, 44, 45, 47, 48, 49, 51, 52, 53, 55, 56, 57, 59, 60, 61, 63, 64, 65, 67, 68, 69, 71, 72, 73,
                        75, 76, 77, 79, 80, 81, 83, 84, 85, 87, 88, 89, 91, 92, 93, 95, 96, 97, 99, 100, 101, 103, 104,
                        105]
    for i in range(number_of_horizontal_bridle):
        mooringLines["bridlesH" + str(y) + "_" + str(x) + "_" + str(i)] = [conject_plate[int(i / 3)],
                                                                           conject_floating[i]]
elif number_of_cage_X == 4 and number_of_cage_Y == 2:
    conject_plate = [16, 15, 20, 21, 17, 16, 21, 22, 18, 17, 22, 23, 19, 18, 23, 24, 21, 20, 25, 26, 22, 21, 26, 27, 23,
                     22, 27, 28, 24, 23, 28, 29]
    start = 62
    conject_floating = []
    for i in range(len(conject_plate)):
        conject_floating.append([start + 1, start + 2, start + 3])
        start += 4
    for i in range(len(conject_plate)):
        for j in range(3):
            mooringLines["bridlesH" + str(y) + "_" + str(x) + "_" + str(i * 3 + j)] = [conject_plate[i],
                                                                                       conject_floating[i][j]]
else:
    print(str(number_of_cage_X) + "x" + str(number_of_cage_Y) + "is not supported now")
    exit()

# arc lines ----> floating collar and bottom ring

hdpePipe = {}
# floating collar
number_of_key_node1 = (number_of_cage_X + 1) * (number_of_cage_Y + 1) * 2 + 2 * (number_of_cage_X + 1) + 2 * (
        number_of_cage_Y + 1) + number_of_cage_X * number_of_cage_Y * 2
number_of_key_node0 = (number_of_cage_X + 1) * (number_of_cage_Y + 1) * 2 + 2 * (number_of_cage_X + 1) + 2 * (
        number_of_cage_Y + 1)
number_of_arc_topring = number_of_floating_segement * (number_of_cage_Y) * (number_of_cage_X)
for y in range(number_of_cage_Y):
    for x in range(number_of_cage_X):
        for i in range(number_of_floating_segement - 1):
            hdpePipe["topRing" + str(y) + "_" + str(x) + "_" + str(i)] = [
                number_of_key_node0 + number_of_cage_X * y + x,
                number_of_key_node1 + number_of_cage_X * number_of_floating_segement * y + number_of_floating_segement * x + i,
                number_of_key_node1 + number_of_cage_X * number_of_floating_segement * y + number_of_floating_segement * x + i + 1]
        hdpePipe["topRing" + str(y) + "_" + str(x) + "_" + str(number_of_floating_segement - 1)] = [
            number_of_key_node0 + number_of_cage_X * y + x,
            number_of_key_node1 + number_of_cage_X * number_of_floating_segement * y + number_of_floating_segement * x + number_of_floating_segement - 1,
            number_of_key_node1 + number_of_cage_X * number_of_floating_segement * y + number_of_floating_segement * x]

# bottom ring
number_of_key_node1 = (number_of_cage_X + 1) * (number_of_cage_Y + 1) * 2 + 2 * (number_of_cage_X + 1) + 2 * (
        number_of_cage_Y + 1) + number_of_cage_X * number_of_cage_Y * 2 + number_of_floating_segement * number_of_cage_X * number_of_cage_Y
number_of_key_node0 = (number_of_cage_X + 1) * (number_of_cage_Y + 1) * 2 + 2 * (number_of_cage_X + 1) + 2 * (
        number_of_cage_Y + 1) + number_of_cage_X * number_of_cage_Y
number_of_arc_bottomring = number_of_floating_segement * (number_of_cage_Y) * (number_of_cage_X)
for y in range(number_of_cage_Y):
    for x in range(number_of_cage_X):
        for i in range(number_of_floating_segement - 1):
            hdpePipe["bottomRing" + str(y) + "_" + str(x) + "_" + str(i)] = [
                number_of_key_node0 + number_of_cage_X * y + x,
                number_of_key_node1 + number_of_cage_X * number_of_floating_segement * y + number_of_floating_segement * x + i,
                number_of_key_node1 + number_of_cage_X * number_of_floating_segement * y + number_of_floating_segement * x + i + 1]
        hdpePipe["bottomRing" + str(y) + "_" + str(x) + "_" + str(number_of_floating_segement - 1)] = [
            number_of_key_node0 + number_of_cage_X * y + x,
            number_of_key_node1 + number_of_cage_X * number_of_floating_segement * y + number_of_floating_segement * x + number_of_floating_segement - 1,
            number_of_key_node1 + number_of_cage_X * number_of_floating_segement * y + number_of_floating_segement * x]

###
### GEOM component
###
import salome

salome.salome_init()
theStudy = salome.myStudy
import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS

geompy = geomBuilder.New(theStudy)
Ver = ["none"] * len(nodesInMooring)
for index, vertex in enumerate(nodesInMooring):
    Ver[index] = geompy.MakeVertex(vertex[0], vertex[1], vertex[2])
    geompy.addToStudy(Ver[index], 'K_' + str(index))

line = ["none"] * len([key for key in mooringLines])
index = 0
for key in mooringLines:
    line[index] = geompy.MakeLineTwoPnt(Ver[mooringLines[key][0]], Ver[mooringLines[key][1]])
    geompy.addToStudy(line[index], key)
    index += 1

arc = ["none"] * len([key for key in hdpePipe])
index = 0
for key in hdpePipe:
    arc[index] = geompy.MakeArcCenter(Ver[hdpePipe[key][0]], Ver[hdpePipe[key][1]], Ver[hdpePipe[key][2]], False)
    geompy.addToStudy(arc[index], key)
    index += 1

Fuse_1 = geompy.MakeFuseList(line + arc, True, True)
geompy.addToStudy(Fuse_1, 'Fuse_1')

# group name of geom


start_edge = 3 * number_of_buoy + 2
frameline = geompy.CreateGroup(Fuse_1, geompy.ShapeType["EDGE"])
geompy.UnionIDs(frameline, [i for i in range(start_edge, start_edge + number_of_frameX + number_of_frameY)])
geompy.addToStudyInFather(Fuse_1, frameline, 'frameline')

start_edge += number_of_frameX + number_of_frameY
anchorline = geompy.CreateGroup(Fuse_1, geompy.ShapeType["EDGE"])
geompy.UnionIDs(anchorline, [i for i in range(start_edge, start_edge + number_of_anchor * 2, 2)])
geompy.addToStudyInFather(Fuse_1, anchorline, 'anchorline')

start_edge += 2 * number_of_anchor
bridleV = geompy.CreateGroup(Fuse_1, geompy.ShapeType["EDGE"])
geompy.UnionIDs(bridleV, [i for i in range(start_edge, start_edge + 3 * number_of_vertical_bridle, 3)])
geompy.addToStudyInFather(Fuse_1, bridleV, 'bridleV')

start_edge += 3 * number_of_vertical_bridle
bridleH = geompy.CreateGroup(Fuse_1, geompy.ShapeType["EDGE"])
geompy.UnionIDs(bridleH, [i for i in range(start_edge, start_edge + number_of_horizontal_bridle)])
geompy.addToStudyInFather(Fuse_1, bridleH, 'bridleH')

buoyline = geompy.CreateGroup(Fuse_1, geompy.ShapeType["EDGE"])
geompy.UnionIDs(buoyline, [i for i in range(2, number_of_buoy * 3, 3)])
geompy.addToStudyInFather(Fuse_1, buoyline, 'buoyline')

number_of_object = len(Ver) + len(line) - 2 * (number_of_cage_X * number_of_cage_Y - 1)

topring = geompy.CreateGroup(Fuse_1, geompy.ShapeType["EDGE"])
geompy.UnionIDs(topring, [i for i in range(number_of_object,
                                           number_of_object + number_of_floating_segement * number_of_cage_X * number_of_cage_Y)])
geompy.addToStudyInFather(Fuse_1, topring, 'topring')

number_of_object += number_of_floating_segement * number_of_cage_X * number_of_cage_Y
bottomring = geompy.CreateGroup(Fuse_1, geompy.ShapeType["EDGE"])
geompy.UnionIDs(bottomring, [i for i in range(number_of_object,
                                              number_of_object + number_of_floating_segement * number_of_cage_X * number_of_cage_Y)])
geompy.addToStudyInFather(Fuse_1, bottomring, 'bottomring')

# ##
# ## SMESH component
# ##


import SMESH, SALOMEDS
from salome.smesh import smeshBuilder

smesh = smeshBuilder.New(theStudy)
Mesh_1 = smesh.Mesh(Fuse_1)

Regular_6 = Mesh_1.Segment()
Regular_3 = Mesh_1.Segment(geom=buoyline)
Regular_2_0 = Mesh_1.Segment(geom=bottomring)
Regular_2_1 = Mesh_1.Segment(geom=topring)
Regular_10 = Mesh_1.Segment(geom=anchorline)

NumberOfSegments_6 = Regular_6.NumberOfSegments(6)
NumberOfSegments_5 = Regular_3.NumberOfSegments(3)
NumberOfSegments_2_0 = Regular_2_0.NumberOfSegments(2)
NumberOfSegments_2_1 = Regular_2_1.NumberOfSegments(2)
NumberOfSegments_10 = Regular_10.NumberOfSegments(10)

isDone = Mesh_1.Compute()
Sub_mesh_1 = Regular_3.GetSubMesh()
Sub_mesh_2_0 = Regular_2_0.GetSubMesh()
Sub_mesh_2_1 = Regular_2_1.GetSubMesh()
Sub_mesh_3 = Regular_6.GetSubMesh()
Sub_mesh_4 = Regular_10.GetSubMesh()

try:
    Mesh_1.ExportDAT(cwd+"/mooring.dat")
    pass
except:
    print('ExportDAT() failed. Invalid file name?')

f = open(cwd+"/mooring.dat", "r")
lines = f.readlines()
f.close()
number_of_nodes_mooring = int(lines[0].split(" ")[0])
number_of_segment_mooring = int(lines[0].split(" ")[1])

for item in lines[1:number_of_nodes_mooring + 1]:
    k = item.split(" ")
    point_mooring.append([float(k[1]), float(k[2]), float(k[3])])

for item in lines[number_of_nodes_mooring + 1:]:
    k = item.split(" ")
    con_mooring.append([int(k[2]) - 1, int(k[3]) - 1])

# generate the point coordinates matrix for cylindrical cage
for y in range(number_of_cage_Y):
    for x in range(number_of_cage_X):
        for j in range(0, NN + 1):
            for i in range(0, NT):
                point_netting.append(
                    [center_floating[y, x][0] + netpen_diameter / 2 * np.cos(i * 2 * np.pi / float(NT)),
                     center_floating[y, x][1] + netpen_diameter / 2 * np.sin(i * 2 * np.pi / float(NT)),
                     center_floating[y, x][2] - j * cage_height / float(NN)])
        for j in range(1, BN):
            for i in range(0, NT):
                point_netting.append(
                    [center_floating[y, x][0] + netpen_diameter / 2 * ((BN - j) / BN) * np.cos(
                        i * 2 * np.pi / float(NT)),
                     center_floating[y, x][1] + netpen_diameter / 2 * ((BN - j) / BN) * np.sin(
                         i * 2 * np.pi / float(NT)),
                     center_floating[y, x][2] - cage_height - j * (cage_cone_height - cage_height) / float(BN)])
        point_netting.append([center_floating[y, x][0],
                              center_floating[y, x][1],
                              -cage_cone_height])  # the last point should be at the cone tip

net_node_number = len(point_netting)
# print(net_node_number)
for each_node in point_netting:
    nodeID = Mesh_1.AddNode(float(each_node[0]), float(each_node[1]), float(each_node[2]))

# >>>>>>>>>>
# Netting line and surface
# >>>>>>>>>>
start_node = number_of_nodes_mooring
for y in range(number_of_cage_Y):
    for x in range(number_of_cage_X):
        # print("startpointis" + str(start_node))
        for i in range(1, NT + 1):
            for j in range(0, BN + NN):
                # the last horizontal line
                if j == BN + NN - 1:
                    if i == NT:
                        edge = Mesh_1.AddEdge([start_node + i + j * NT,
                                               start_node + 1 + i + (
                                                       j - 1) * NT])  # add the horizontal line into geometry
                        con_netting.append([start_node + i + j * NT - 1,
                                            start_node + 1 + i + (j - 1) * NT - 1])  # add the horizontal line into con
                    else:
                        edge = Mesh_1.AddEdge([start_node + i + j * NT,
                                               start_node + 1 + i + j * NT])  # add the horizontal line into geometry
                        con_netting.append([start_node + i + j * NT - 1,
                                            start_node + 1 + i + j * NT - 1])  # add the horizontal line into con
                # the rest lines and all vertical surfaces
                else:
                    edge = Mesh_1.AddEdge([start_node + i + j * NT,
                                           start_node + i + (j + 1) * NT])  # add the vertical line into geometry
                    con_netting.append([start_node + i + j * NT - 1,
                                        start_node + i + (j + 1) * NT - 1])  # add the vertical line into con
                    if i == NT:
                        edge = Mesh_1.AddEdge([start_node + i + j * NT,
                                               start_node + 1 + i + (
                                                       j - 1) * NT])  # add the horizontal line into geometry
                        con_netting.append([start_node + i + j * NT - 1,
                                            start_node + 1 + i + (j - 1) * NT - 1])  # add the horizontal line into con
                        sur_netting.append([start_node + i + j * NT - 1,
                                            start_node + 1 + i + (j - 1) * NT - 1,
                                            start_node + i + (j + 1) * NT - 1,
                                            start_node + 1 + i + j * NT - 1])
                    else:
                        edge = Mesh_1.AddEdge([start_node + i + j * NT,
                                               start_node + 1 + i + j * NT])  # add the horizontal line into geometry
                        con_netting.append([start_node + i + j * NT - 1,
                                            start_node + 1 + i + j * NT - 1])  # add the horizontal line into con
                        sur_netting.append([start_node + i + j * NT - 1,
                                            start_node + 1 + i + j * NT - 1,
                                            start_node + i + (j + 1) * NT - 1,
                                            start_node + 1 + i + (j + 1) * NT - 1])
        start_node += (NT * (BN + NN) + 1)
        for k in range(1, NT + 1):
            edge = Mesh_1.AddEdge([start_node,
                                   start_node - k])  # add the horizontal line into geometry
            con_netting.append([start_node - 1,
                                start_node - k - 1])  # add the horizontal line into con
            if k == NT:
                sur_netting.append([start_node - 1,
                                    start_node - k - 1,
                                    start_node - 2])
            else:
                sur_netting.append([start_node - 1,
                                    start_node - k - 1,
                                    start_node - k - 2])

# link
# top connect
# ! #FIXME: stupid method. the lists are changed according the numbeing in GUI
if number_of_cage_X == 1 and number_of_cage_Y == 1:
    connet_mooring = [17, 289, 19, 290, 21, 291, 23, 292, 25, 293, 27, 294, 29, 295, 31, 296, 33, 297, 35, 298, 37, 299,
                      39,
                      300, 41, 301, 43, 302, 45, 303, 47, 304]
    connet_netting = [321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339,
                      340,
                      341, 342, 343, 344, 345, 346, 347, 348, 349, 350, 351, 352]
    for i in range(len(connet_mooring)):
        edge = Mesh_1.AddEdge([connet_mooring[i], connet_netting[i]])  # add the horizontal line into geometry

    connet_mooring = [18, 305, 20, 306, 22, 307, 24, 308, 26, 309, 28, 310, 30, 311, 32, 312, 34, 313, 36, 314, 38, 315,
                      40,
                      316, 42, 317, 44, 318, 46, 319, 48, 320]
    connet_netting = [481, 482, 483, 484, 485, 486, 487, 488, 489, 490, 491, 492, 493, 494, 495, 496, 497, 498, 499,
                      500,
                      501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 512]
    for i in range(len(connet_mooring)):
        edge = Mesh_1.AddEdge([connet_mooring[i], connet_netting[i]])  # add the horizontal line into geometry
        # con_mooring.append([connet_mooring[i]-1, connet_netting[i]-1]) # It might has only small effect on the hydordynamic responses

elif number_of_cage_X == 4 and number_of_cage_Y == 1:

    connet_mooring = [35, 934, 37, 935, 39, 936, 41, 937, 43, 938, 45, 939, 47, 940, 49, 941, 51, 942, 53, 943, 55, 944,
                      57, 945, 59, 946, 61, 947, 63, 948, 65, 949]
    connet_netting = [1062, 1063, 1064, 1065, 1066, 1067, 1068, 1069, 1070, 1071, 1072, 1073, 1074, 1075, 1076, 1077,
                      1078, 1079, 1080, 1081, 1082, 1083, 1084, 1085, 1086, 1087, 1088, 1089, 1090, 1091, 1092, 1093]
    for i in range(len(connet_mooring)):
        edge = Mesh_1.AddEdge([connet_mooring[i], connet_netting[i]])  # add the horizontal line into geometry

    connet_mooring = [36, 998, 38, 999, 40, 1000, 42, 1001, 44, 1002, 46, 1003, 48, 1004, 50, 1005, 52, 1006, 54, 1007,
                      56, 1008, 58, 1009, 60, 1010, 62, 1011, 64, 1012, 66, 1013]
    connet_netting = [1222, 1223, 1224, 1225, 1226, 1227, 1228, 1229, 1230, 1231, 1232, 1233, 1234, 1235, 1236, 1237,
                      1238, 1239, 1240, 1241, 1242, 1243, 1244, 1245, 1246, 1247, 1248, 1249, 1250, 1251, 1252, 1253]
    for i in range(len(connet_mooring)):
        edge = Mesh_1.AddEdge([connet_mooring[i], connet_netting[i]])  # add the horizontal line into geometry

    connet_mooring = [67, 950, 69, 951, 71, 952, 73, 953, 75, 954, 77, 955, 79, 956, 81, 957, 83, 958, 85, 959, 87, 960,
                      89, 961, 91, 962, 93, 963, 95, 964, 97, 965]
    connet_netting = [1383, 1384, 1385, 1386, 1387, 1388, 1389, 1390, 1391, 1392, 1393, 1394, 1395, 1396, 1397, 1398,
                      1399, 1400, 1401, 1402, 1403, 1404, 1405, 1406, 1407, 1408, 1409, 1410, 1411, 1412, 1413, 1414]
    for i in range(len(connet_mooring)):
        edge = Mesh_1.AddEdge([connet_mooring[i], connet_netting[i]])  # add the horizontal line into geometry

    connet_mooring = [68, 1014, 70, 1015, 72, 1016, 74, 1017, 76, 1018, 78, 1019, 80, 1020, 82, 1021, 84, 1022, 86,
                      1023, 88, 1024, 90, 1025, 92, 1026, 94, 1027, 96, 1028, 98, 1029]
    connet_netting = [1543, 1544, 1545, 1546, 1547, 1548, 1549, 1550, 1551, 1552, 1553, 1554, 1555, 1556, 1557, 1558,
                      1559, 1560, 1561, 1562, 1563, 1564, 1565, 1566, 1567, 1568, 1569, 1570, 1571, 1572, 1573, 1574]
    for i in range(len(connet_mooring)):
        edge = Mesh_1.AddEdge([connet_mooring[i], connet_netting[i]])  # add the horizontal line into geometry

    connet_mooring = [99, 966, 101, 967, 103, 968, 105, 969, 107, 970, 109, 971, 111, 972, 113, 973, 115, 974, 117, 975,
                      119, 976, 121, 977, 123, 978, 125, 979, 127, 980, 129, 981]
    connet_netting = [1704, 1705, 1706, 1707, 1708, 1709, 1710, 1711, 1712, 1713, 1714, 1715, 1716, 1717, 1718, 1719,
                      1720, 1721, 1722, 1723, 1724, 1725, 1726, 1727, 1728, 1729, 1730, 1731, 1732, 1733, 1734, 1735]
    for i in range(len(connet_mooring)):
        edge = Mesh_1.AddEdge([connet_mooring[i], connet_netting[i]])  # add the horizontal line into geometry

    connet_mooring = [100, 1030, 102, 1031, 104, 1032, 106, 1033, 108, 1034, 110, 1035, 112, 1036, 114, 1037, 116, 1038,
                      118, 1039, 120, 1040, 122, 1041, 124, 1042, 126, 1043, 128, 1044, 130, 1045]
    connet_netting = [1864, 1865, 1866, 1867, 1868, 1869, 1870, 1871, 1872, 1873, 1874, 1875, 1876, 1877, 1878, 1879,
                      1880, 1881, 1882, 1883, 1884, 1885, 1886, 1887, 1888, 1889, 1890, 1891, 1892, 1893, 1894, 1895]
    for i in range(len(connet_mooring)):
        edge = Mesh_1.AddEdge([connet_mooring[i], connet_netting[i]])  # add the horizontal line into geometry

    connet_mooring = [131, 982, 133, 983, 135, 984, 137, 985, 139, 986, 141, 987, 143, 988, 145, 989, 147, 990, 149,
                      991, 151, 992, 153, 993, 155, 994, 157, 995, 159, 996, 161, 997]
    connet_netting = [2025, 2026, 2027, 2028, 2029, 2030, 2031, 2032, 2033, 2034, 2035, 2036, 2037, 2038, 2039, 2040,
                      2041, 2042, 2043, 2044, 2045, 2046, 2047, 2048, 2049, 2050, 2051, 2052, 2053, 2054, 2055, 2056]
    for i in range(len(connet_mooring)):
        edge = Mesh_1.AddEdge([connet_mooring[i], connet_netting[i]])  # add the horizontal line into geometry

    connet_mooring = [132, 1046, 134, 1047, 136, 1048, 138, 1049, 140, 1050, 142, 1051, 144, 1052, 146, 1053, 148, 1054,
                      150, 1055, 152, 1056, 154, 1057, 156, 1058, 158, 1059, 160, 1060, 162, 1061]
    connet_netting = [2185, 2186, 2187, 2188, 2189, 2190, 2191, 2192, 2193, 2194, 2195, 2196, 2197, 2198, 2199, 2200,
                      2201, 2202, 2203, 2204, 2205, 2206, 2207, 2208, 2209, 2210, 2211, 2212, 2213, 2214, 2215, 2216]
    for i in range(len(connet_mooring)):
        edge = Mesh_1.AddEdge([connet_mooring[i], connet_netting[i]])  # add the horizontal line into geometry

elif number_of_cage_X == 4 and number_of_cage_Y == 2:
    # no1
    connet_mooring = [47, 1707, 49, 1708, 51, 1709, 53, 1710, 55, 1711, 57, 1712, 59, 1713, 61, 1714, 63, 1715, 65,
                      1716, 67, 1717, 69, 1718, 71, 1719, 73, 1720, 75, 1721, 77, 1722]
    connet_netting = [1963, 1964, 1965, 1966, 1967, 1968, 1969, 1970, 1971, 1972, 1973, 1974, 1975, 1976, 1977, 1978,
                      1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994]
    for i in range(len(connet_mooring)):
        edge = Mesh_1.AddEdge([connet_mooring[i], connet_netting[i]])  # add the horizontal line into geometry

    connet_mooring = [48, 1835, 50, 1836, 52, 1837, 54, 1838, 56, 1839, 58, 1840, 60, 1841, 62, 1842, 64, 1843, 66,
                      1844, 68, 1845, 70, 1846, 72, 1847, 74, 1848, 76, 1849, 78, 1850]
    connet_netting = [2123, 2124, 2125, 2126, 2127, 2128, 2129, 2130, 2131, 2132, 2133, 2134, 2135, 2136, 2137, 2138,
                      2139, 2140, 2141, 2142, 2143, 2144, 2145, 2146, 2147, 2148, 2149, 2150, 2151, 2152, 2153, 2154]
    for i in range(len(connet_mooring)):
        edge = Mesh_1.AddEdge([connet_mooring[i], connet_netting[i]])  # add the horizontal line into geometry
    # no2
    connet_mooring = [79, 1723, 81, 1724, 83, 1725, 85, 1726, 87, 1727, 89, 1728, 91, 1729, 93, 1730, 95, 1731, 97,
                      1732, 99, 1733, 101, 1734, 103, 1735, 105, 1736, 107, 1737, 109, 1738]
    connet_netting = [2284, 2285, 2286, 2287, 2288, 2289, 2290, 2291, 2292, 2293, 2294, 2295, 2296, 2297, 2298, 2299,
                      2300, 2301, 2302, 2303, 2304, 2305, 2306, 2307, 2308, 2309, 2310, 2311, 2312, 2313, 2314, 2315]
    for i in range(len(connet_mooring)):
        edge = Mesh_1.AddEdge([connet_mooring[i], connet_netting[i]])  # add the horizontal line into geometry

    connet_mooring = [80, 1851, 82, 1852, 84, 1853, 86, 1854, 88, 1855, 90, 1856, 92, 1857, 94, 1858, 96, 1859, 98,
                      1860, 100, 1861, 102, 1862, 104, 1863, 106, 1864, 108, 1865, 110, 1866]
    connet_netting = [2444, 2445, 2446, 2447, 2448, 2449, 2450, 2451, 2452, 2453, 2454, 2455, 2456, 2457, 2458, 2459,
                      2460, 2461, 2462, 2463, 2464, 2465, 2466, 2467, 2468, 2469, 2470, 2471, 2472, 2473, 2474, 2475]
    for i in range(len(connet_mooring)):
        edge = Mesh_1.AddEdge([connet_mooring[i], connet_netting[i]])  # add the horizontal line into geometry
    # no3
    connet_mooring = [111, 1739, 113, 1740, 115, 1741, 117, 1742, 119, 1743, 121, 1744, 123, 1745, 125, 1746, 127, 1747,
                      129, 1748, 131, 1749, 133, 1750, 135, 1751, 137, 1752, 139, 1753, 141, 1754]
    connet_netting = [2605, 2606, 2607, 2608, 2609, 2610, 2611, 2612, 2613, 2614, 2615, 2616, 2617, 2618, 2619, 2620,
                      2621, 2622, 2623, 2624, 2625, 2626, 2627, 2628, 2629, 2630, 2631, 2632, 2633, 2634, 2635, 2636]
    for i in range(len(connet_mooring)):
        edge = Mesh_1.AddEdge([connet_mooring[i], connet_netting[i]])  # add the horizontal line into geometry

    connet_mooring = [112, 1867, 114, 1868, 116, 1869, 118, 1870, 120, 1871, 122, 1872, 124, 1873, 126, 1874, 128, 1875,
                      130, 1876, 132, 1877, 134, 1878, 136, 1879, 138, 1880, 140, 1881, 142, 1882]
    connet_netting = [2765, 2766, 2767, 2768, 2769, 2770, 2771, 2772, 2773, 2774, 2775, 2776, 2777, 2778, 2779, 2780,
                      2781, 2782, 2783, 2784, 2785, 2786, 2787, 2788, 2789, 2790, 2791, 2792, 2793, 2794, 2795, 2796]
    for i in range(len(connet_mooring)):
        edge = Mesh_1.AddEdge([connet_mooring[i], connet_netting[i]])  # add the horizontal line into geometry
    # no4
    connet_mooring = [143, 1755, 145, 1756, 147, 1757, 149, 1758, 151, 1759, 153, 1760, 155, 1761, 157, 1762, 159, 1763,
                      161, 1764, 163, 1765, 165, 1766, 167, 1767, 169, 1768, 171, 1769, 173, 1770]
    connet_netting = [2926, 2927, 2928, 2929, 2930, 2931, 2932, 2933, 2934, 2935, 2936, 2937, 2938, 2939, 2940, 2941,
                      2942, 2943, 2944, 2945, 2946, 2947, 2948, 2949, 2950, 2951, 2952, 2953, 2954, 2955, 2956, 2957]
    for i in range(len(connet_mooring)):
        edge = Mesh_1.AddEdge([connet_mooring[i], connet_netting[i]])  # add the horizontal line into geometry

    connet_mooring = [144, 1883, 146, 1884, 148, 1885, 150, 1886, 152, 1887, 154, 1888, 156, 1889, 158, 1890, 160, 1891,
                      162, 1892, 164, 1893, 166, 1894, 168, 1895, 170, 1896, 172, 1897, 174, 1898]
    connet_netting = [3086, 3087, 3088, 3089, 3090, 3091, 3092, 3093, 3094, 3095, 3096, 3097, 3098, 3099, 3100, 3101,
                      3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3113, 3114, 3115, 3116, 3117]
    for i in range(len(connet_mooring)):
        edge = Mesh_1.AddEdge([connet_mooring[i], connet_netting[i]])  # add the horizontal line into geometry
    # no5
    connet_mooring = [175, 1771, 177, 1772, 179, 1773, 181, 1774, 183, 1775, 185, 1776, 187, 1777, 189, 1778, 191, 1779,
                      193, 1780, 195, 1781, 197, 1782, 199, 1783, 201, 1784, 203, 1785, 205, 1786]
    connet_netting = [3247, 3248, 3249, 3250, 3251, 3252, 3253, 3254, 3255, 3256, 3257, 3258, 3259, 3260, 3261, 3262,
                      3263, 3264, 3265, 3266, 3267, 3268, 3269, 3270, 3271, 3272, 3273, 3274, 3275, 3276, 3277, 3278]
    for i in range(len(connet_mooring)):
        edge = Mesh_1.AddEdge([connet_mooring[i], connet_netting[i]])  # add the horizontal line into geometry

    connet_mooring = [176, 1899, 178, 1900, 180, 1901, 182, 1902, 184, 1903, 186, 1904, 188, 1905, 190, 1906, 192, 1907,
                      194, 1908, 196, 1909, 198, 1910, 200, 1911, 202, 1912, 204, 1913, 206, 1914]
    connet_netting = [3407, 3408, 3409, 3410, 3411, 3412, 3413, 3414, 3415, 3416, 3417, 3418, 3419, 3420, 3421, 3422,
                      3423, 3424, 3425, 3426, 3427, 3428, 3429, 3430, 3431, 3432, 3433, 3434, 3435, 3436, 3437, 3438]
    for i in range(len(connet_mooring)):
        edge = Mesh_1.AddEdge([connet_mooring[i], connet_netting[i]])  # add the horizontal line into geometry
    # no6
    connet_mooring = [207, 1787, 209, 1788, 211, 1789, 213, 1790, 215, 1791, 217, 1792, 219, 1793, 221, 1794, 223, 1795,
                      225, 1796, 227, 1797, 229, 1798, 231, 1799, 233, 1800, 235, 1801, 237, 1802]
    connet_netting = [3568, 3569, 3570, 3571, 3572, 3573, 3574, 3575, 3576, 3577, 3578, 3579, 3580, 3581, 3582, 3583,
                      3584, 3585, 3586, 3587, 3588, 3589, 3590, 3591, 3592, 3593, 3594, 3595, 3596, 3597, 3598, 3599]
    for i in range(len(connet_mooring)):
        edge = Mesh_1.AddEdge([connet_mooring[i], connet_netting[i]])  # add the horizontal line into geometry

    connet_mooring = [208, 1915, 210, 1916, 212, 1917, 214, 1918, 216, 1919, 218, 1920, 220, 1921, 222, 1922, 224, 1923,
                      226, 1924, 228, 1925, 230, 1926, 232, 1927, 234, 1928, 236, 1929, 238, 1930]
    connet_netting = [3728, 3729, 3730, 3731, 3732, 3733, 3734, 3735, 3736, 3737, 3738, 3739, 3740, 3741, 3742, 3743,
                      3744, 3745, 3746, 3747, 3748, 3749, 3750, 3751, 3752, 3753, 3754, 3755, 3756, 3757, 3758, 3759]
    for i in range(len(connet_mooring)):
        edge = Mesh_1.AddEdge([connet_mooring[i], connet_netting[i]])  # add the horizontal line into geometry
    # no7
    connet_mooring = [239, 1803, 241, 1804, 243, 1805, 245, 1806, 247, 1807, 249, 1808, 251, 1809, 253, 1810, 255, 1811,
                      257, 1812, 259, 1813, 261, 1814, 263, 1815, 265, 1816, 267, 1817, 269, 1818]
    connet_netting = [3889, 3890, 3891, 3892, 3893, 3894, 3895, 3896, 3897, 3898, 3899, 3900, 3901, 3902, 3903, 3904,
                      3905, 3906, 3907, 3908, 3909, 3910, 3911, 3912, 3913, 3914, 3915, 3916, 3917, 3918, 3919, 3920]
    for i in range(len(connet_mooring)):
        edge = Mesh_1.AddEdge([connet_mooring[i], connet_netting[i]])  # add the horizontal line into geometry

    connet_mooring = [240, 1931, 242, 1932, 244, 1933, 246, 1934, 248, 1935, 250, 1936, 252, 1937, 254, 1938, 256, 1939,
                      258, 1940, 260, 1941, 262, 1942, 264, 1943, 266, 1944, 268, 1945, 270, 1946]
    connet_netting = [4049, 4050, 4051, 4052, 4053, 4054, 4055, 4056, 4057, 4058, 4059, 4060, 4061, 4062, 4063, 4064,
                      4065, 4066, 4067, 4068, 4069, 4070, 4071, 4072, 4073, 4074, 4075, 4076, 4077, 4078, 4079, 4080]
    for i in range(len(connet_mooring)):
        edge = Mesh_1.AddEdge([connet_mooring[i], connet_netting[i]])  # add the horizontal line into geometry
    # no8
    connet_mooring = [271, 1819, 273, 1820, 275, 1821, 277, 1822, 279, 1823, 281, 1824, 283, 1825, 285, 1826, 287, 1827,
                      289, 1828, 291, 1829, 293, 1830, 295, 1831, 297, 1832, 299, 1833, 301, 1834]
    connet_netting = [4210, 4211, 4212, 4213, 4214, 4215, 4216, 4217, 4218, 4219, 4220, 4221, 4222, 4223, 4224, 4225,
                      4226, 4227, 4228, 4229, 4230, 4231, 4232, 4233, 4234, 4235, 4236, 4237, 4238, 4239, 4240, 4241]
    for i in range(len(connet_mooring)):
        edge = Mesh_1.AddEdge([connet_mooring[i], connet_netting[i]])  # add the horizontal line into geometry

    connet_mooring = [272, 1947, 274, 1948, 276, 1949, 278, 1950, 280, 1951, 282, 1952, 284, 1953, 286, 1954, 288, 1955,
                      290, 1956, 292, 1957, 294, 1958, 296, 1959, 298, 1960, 300, 1961, 302, 1962]
    connet_netting = [4370, 4371, 4372, 4373, 4374, 4375, 4376, 4377, 4378, 4379, 4380, 4381, 4382, 4383, 4384, 4385,
                      4386, 4387, 4388, 4389, 4390, 4391, 4392, 4393, 4394, 4395, 4396, 4397, 4398, 4399, 4400, 4401]
    for i in range(len(connet_mooring)):
        edge = Mesh_1.AddEdge([connet_mooring[i], connet_netting[i]])  # add the horizontal line into geometry

else:
    print(str(number_of_cage_X) + "x" + str(number_of_cage_Y) + "is not supported now")
    exit()

# name node
# naming  the group
# naming the node
# GROUP_NO

buoy = Mesh_1.CreateEmptyGroup(SMESH.NODE, 'buoy')
nbAdd = buoy.Add([i for i in range(1, 1 + number_of_buoy * 2, 2)])
smesh.SetName(buoy, 'buoy')

plate = Mesh_1.CreateEmptyGroup(SMESH.NODE, 'plate')
nbAdd = plate.Add([i for i in range(2, 2 + number_of_buoy * 2, 2)])
smesh.SetName(plate, 'plate')

anchor = Mesh_1.CreateEmptyGroup(SMESH.NODE, 'anchor')
nbAdd = anchor.Add([i for i in range(1 + number_of_buoy * 2, 1 + number_of_buoy * 2 + number_of_anchor)])
smesh.SetName(anchor, 'anchor')

net_tip = Mesh_1.CreateEmptyGroup(SMESH.NODE, 'net_tip')
nbAdd = net_tip.Add([i for i in range(1 + number_of_nodes_mooring + (NT * (BN + NN)),
                                      number_of_nodes_mooring + net_node_number + 1, (NT * (BN + NN) + 1))])
smesh.SetName(net_tip, 'net_tip')

topnodes = Mesh_1.CreateEmptyGroup(SMESH.NODE, 'net_top')
start_node = number_of_nodes_mooring
for y in range(number_of_cage_Y):
    for x in range(number_of_cage_X):
        nbAdd = topnodes.Add([i for i in range(start_node + 1, start_node + 1 + NT)])
        start_node += (NT * (BN + NN) + 1)
smesh.SetName(topnodes, 'net_top')

net_nodes = Mesh_1.CreateEmptyGroup(SMESH.NODE, 'net_nodes')
nbAdd = net_nodes.Add([i for i in range(number_of_nodes_mooring + 1,
                                        number_of_nodes_mooring + 1 + number_of_cage_X * number_of_cage_Y * (
                                                1 + (NT * (BN + NN))))])
smesh.SetName(net_nodes, 'net_nodes')

allnodes = Mesh_1.CreateEmptyGroup(SMESH.NODE, 'allnodes')
nbAdd = allnodes.AddFrom(Mesh_1.GetMesh())
smesh.SetName(allnodes, 'allnodes')

for i in range(1, number_of_nodes_mooring + net_node_number + 1):
    node1 = Mesh_1.CreateEmptyGroup(SMESH.NODE, 'node%s' % i)
    nbAdd = node1.Add([i])
    smesh.SetName(node1, 'node%s' % i)

# GROUP_MA
# name lines

goupMA = Mesh_1.GroupOnGeom(topring, 'topRings', SMESH.EDGE)
smesh.SetName(goupMA, 'topRings')

goupMA = Mesh_1.GroupOnGeom(bottomring, 'bottomRings', SMESH.EDGE)
smesh.SetName(goupMA, 'bottomRings')

goupMA = Mesh_1.GroupOnGeom(anchorline, 'anchorLines', SMESH.EDGE)
smesh.SetName(goupMA, 'anchorLines')

goupMA = Mesh_1.GroupOnGeom(frameline, 'frameLines', SMESH.EDGE)
smesh.SetName(goupMA, 'frameLines')

goupMA = Mesh_1.GroupOnGeom(bridleH, 'bridlesH', SMESH.EDGE)
smesh.SetName(goupMA, 'bridlesH')

goupMA = Mesh_1.GroupOnGeom(bridleV, 'bridlesV', SMESH.EDGE)
smesh.SetName(goupMA, 'bridlesV')

goupMA = Mesh_1.GroupOnGeom(buoyline, 'buoyLines', SMESH.EDGE)
smesh.SetName(goupMA, 'buoyLines')

twine = Mesh_1.CreateEmptyGroup(SMESH.EDGE, 'twine')
nbAdd = twine.Add([i for i in range(number_of_segment_mooring + 1, number_of_segment_mooring + len(con_netting) + 1)])
smesh.SetName(twine, 'twines')

link = Mesh_1.CreateEmptyGroup(SMESH.EDGE, 'link')
nbAdd = link.Add([i for i in range(number_of_segment_mooring + len(con_netting) + 1, number_of_segment_mooring + len(
    con_netting) + 1 + NT * 2 * number_of_cage_Y * number_of_cage_X)])
smesh.SetName(link, 'links')

meshname = "fishFarm_" + str(number_of_cage_X) + "_" + str(number_of_cage_Y) + ".med"

meshinfo = {
    "Nodes_mooring": point_mooring,
    "Lines_mooring": con_mooring,
    "numberOfNodes_mooring": len(point_mooring),
    "numberOfLines_mooring": len(con_mooring),
    "horizontalElementLength": float(np.pi * floating_diameter / float(NT)),  # for lamda1
    "verticalElementLength": float(cage_height / float(NN)),  # for lamda2
    "NN": NN,
    "NT": NT,
    "Nodes_netting": point_netting,
    "Lines_netting": con_netting,
    "surfs_netting": sur_netting,
    "numberOfNodes_netting": len(point_netting),
    "numberOfLines_netting": len(con_netting),
    "numberOfsurfs_netting": len(sur_netting),
    "meshName": meshname,
}

print("\n"
      "  --------------------------------------\n"
      "  --     University of Stavanger      --\n"
      "  --         Hui Cheng (PhD student)  --\n"
      "  --       Lin Li (Medveileder)       --\n"
      "  --  Prof. Muk Chen Ong (supervisor) --\n"
      "  --------------------------------------\n"
      "  Any questions about this code,\n"
      "  please email: hui.cheng@uis.no\n")

print("<<<<<<<<<< Mesh Information >>>>>>>>>>")
print("Number of node on netting is " + str(meshinfo["numberOfNodes_netting"]) + ".")
print("Number of line on netting is " + str(meshinfo["numberOfLines_netting"]) + ".")
print("Number of surface on netting is " + str(meshinfo["numberOfsurfs_netting"]) + ".\n")

with open(cwd + "/meshInformation.py", 'w') as f:
    f.write("meshinfo=")
    f.write(str(meshinfo))
f.close()

try:
    Mesh_1.ExportMED(cwd + "/" + meshname)
    pass
except:
    print('ExportMED() failed. Invalid file name?')
