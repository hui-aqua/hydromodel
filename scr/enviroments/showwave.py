# import seacondition as sea
from scr.enviroments import seacondition as sea
import numpy as np
import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation

wave1 = sea.Airywave(1.91, 125, 20)
wave2 = sea.Stocks2wave(1.91, 125, 20)
print(wave1)
print(wave2)
t = 0
posi = np.array((0, 0, 0))
print("velocity with airy wave theory = ", wave1.Get_Velo(posi, 1))
print("velocity with stokes 2nd wave thory= ", wave2.Get_Velo(posi, 1))
# 2D domino

domix = np.linspace(0, 500, 50 + 1)
domiy = np.linspace(-10, 10, 21)
domiz = np.linspace(0, -20, 50 + 1)
T = 0
wf = np.array((0))
wf2 = np.array((0))
x = []
z = []
x2 = []
z2 = []

Vx = []
Vz = []
Vx2 = []
Vz2 = []

for i in range(len(domix)):
    wf = np.vstack((wf, wave1.Get_Surface(np.array((domix[i], 0, 0)), T)))
    wf2 = np.vstack((wf2, wave2.Get_Surface(np.array((domix[i], 0, 0)), T)))
    x.append(domix[i])
    z.append(domiz[3])
    posi = np.array((domix[i], domiy[10], domiz[3]))
    Vx.append(wave1.Get_Velo(posi, T)[0])
    Vz.append(wave1.Get_Velo(posi, T)[2])
    x2.append(domix[0])
    z2.append(domiz[i])
    posi = np.array((domix[0], domiy[10], domiz[i]))
    Vx2.append(wave1.Get_Velo(posi, T)[0])
    Vz2.append(wave1.Get_Velo(posi, T)[2])

wf = np.delete(wf, obj=0, axis=0)
wf2 = np.delete(wf2, obj=0, axis=0)
plt.figure()
plt.plot(domix, wf)
plt.plot(domix, wf2)

plt.quiver(x, z, Vx, Vz)
plt.quiver(x2, z2, Vx2, Vz2)

plt.xlabel("X (m)")
plt.ylabel("Z (m)")
plt.xlim(0, 500)
plt.ylim(-20, 6)
plt.show()
