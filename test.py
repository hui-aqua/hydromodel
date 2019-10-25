import numpy as np
from numpy import pi
import matplotlib.pyplot as plt
Sn = 0.35


def fh1(Sn, cosalpha, sinalpha):
    Cd = 0.04 + (-0.04 + Sn - 1.24 * pow(Sn, 2) +
                 13.7 * pow(Sn, 3)) * cosalpha
    Cl = (0.57 * Sn - 3.54 * pow(Sn, 2) +
          10.1 * pow(Sn, 3)) * 2 * sinalpha * cosalpha
    pass

A =(-0.04 + Sn - 1.24 * pow(Sn, 2) +
                 13.7 * pow(Sn, 3))
print("ratio for s1=",(0.02*pi+A)/(0.04+A))
print(0.26/0.215)

x=np.linspace(1, 200)
plt.subplot(projection='polar')
plt.scatter(x,x,marker='.')
plt.show()