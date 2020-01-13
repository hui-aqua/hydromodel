# generate input file for codeAster
import os
import workPath
import numpy as np
import pickle

# cwd = os.getcwd()
if os.path.exists('meshinfomation.txt'):
    with open('meshinfomation.txt', 'r') as f:
        content = f.read()
        meshinfo = eval(content)
else:
    with open('./asterinput/meshinfomation.txt', 'r') as f:
        content = f.read()
        meshinfo = eval(content)

numOfSurface = meshinfo['numberOfSurfaces'] * 4
f = open("../velocityOnNetpanels.dat", "r")
lines = f.readlines()
velocitydict = {}
velocitydict['Numoflist'] = 0
for line in lines:
    if str(numOfSurface) + '\n' in line:
        velocitydict['Numoflist'] += 1

for time in range(velocitydict['Numoflist']):
    dataofvelocity = lines[3 + time * 1157:1155 + time * 1157]
    velocity = []
    for item in dataofvelocity:
        vector = item.split()
        velocity.append([float(vector[0][1:]), float(vector[1]), float(vector[2][:-1])])
    velocitydict['velocityinsurfaceAt' + str(time + 1)] = velocity
f.close()

output = open('velocityfile.pkl', 'wb')
pickle.dump(velocitydict, output)
output.close()

pkfile = open('velocityfile.pkl', 'rb')
re = pickle.load(pkfile)
pkfile.close()

Velo = re['velocityinsurfaceAt' + str(re['Numoflist'])]
T = re['Numoflist'] * 0.1

data = {'Time': T,
        'velo': Velo}

output = open('velo.pkl', 'wb')
pickle.dump(data, output)
output.close()
