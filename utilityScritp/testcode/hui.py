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

point = []
number = 24
for i in range(number):
    point.append([6.5 * np.cos(i * 2 * np.pi / number), 6.5 * np.sin(i * 2 * np.pi / number), 0])
for each in point:
    print('%.4f,  %.4f,  %.4f' % (each[0], each[1], each[2]))
