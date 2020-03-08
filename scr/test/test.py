"""
/--------------------------------\
|    University of Stavanger     |
|           Hui Cheng            |
\--------------------------------/
Any questions about this code, please email: hui.cheng@uis.no

"""
import os
import sys
import numpy as np
import time
import scr.forcemodel.fsimapping2 as fs
cwd="/home/hui/FSI/threecage2/constant/"
print(time.time())
v1= fs.get_velocity(cwd,2345,0.01)
print(time.time())
v2=fs.get_velocity(cwd,2345,0.02)
velocity_dict=fs.velocity_dict
print(time.time())
v3=fs.get_velocity(cwd,2345,0.03)
print(time.time())
