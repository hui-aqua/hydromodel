"""
-------------------------------------------\n
-         University of Stavanger          \n
-         Hui Cheng (PhD student)          \n
-          Lin Li (Medveileder)            \n
-      Prof. Muk Chen Ong (Supervisor)     \n
-------------------------------------------\n
Any questions about this code,
please email: hui.cheng@uis.no \n
"""
import time
import os
import numpy as np

cwd = os.getcwd()


def updatedata(T):
    force = np.zeros((T, 3))
    for i in range(T):
        force[i] = np.array([i, i * i, np.sqrt(i)])
    return force


def writedata(data, time, cwd):
    # totalforce = np.array([time, data[:, 0].mean(), data[:, 1].mean(), data[:, 2].mean()])
    totalforce = [time, data[:, 0].mean(), data[:, 1].mean(), data[:, 2].mean()]
    output_file = open(cwd + 'forceOnNetting.txt', 'a+')
    output_file.write(str(totalforce) + '\n')
    output_file.close()


print(cwd)
for i in range(5, 10, 1):
    k = updatedata(i)
    print("the k is " + str(k))
    writedata(k, i, cwd)
