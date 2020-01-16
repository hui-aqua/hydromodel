"""
/--------------------------------\
|    University of Stavanger     |
|           Hui Cheng            |
\--------------------------------/
Any questions about this code, please email: hui.cheng@uis.no

Fish cage is along the Z- direction
Z=0 is the free surface
Z<0 is the water zone
Z>0 is the air zone

Run with a arguement [casename]
"""
import sys
import os
import numpy as np
from numpy import pi

cwd = os.getcwd()
Dictname = str(sys.argv[1])
with open(Dictname, 'r') as f:
    content = f.read()
    cageinfo = eval(content)
