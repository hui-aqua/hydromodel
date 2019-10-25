import seacondition as sea
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

wave1 = sea.Airywave(4.91, 125, 16)
wave2 = sea.Stocks2wave(4.91, 125, 16)
print(wave1)
print(wave2)
t = 0
posi = np.array((0, 0, 0))
velo = wave1.Get_Velo(posi, 1)
print("velocity = ", velo)

# 2D domino

domix = np.linspace(0, 500, 2 * 50 + 1)
domiy = np.linspace(-10, 10, 21)
domiz = np.linspace(0, -50, 10 + 1)
T = 0
wf = np.array((0))
wf2 = np.array((0))
x = []
y = []
z = []
waveV = []
Vx = []
Vz = []
for i in range(len(domix)):
    wf = np.vstack((wf, wave1.Get_Surface(np.array((domix[i], 0, 0)), T)))
    wf2 = np.vstack((wf2, wave2.Get_Surface(np.array((domix[i], 0, 0)), T)))
    x.append(domix[i])
    y.append(domiy[10])
    z.append(domiz[1])
    posi = np.array((domix[i], domiy[10], domiz[1]))
    waveV.append(wave1.Get_Velo(posi, T))
    Vx.append(wave1.Get_Velo(posi, T)[0])
    Vz.append(wave1.Get_Velo(posi, T)[2])
wf = np.delete(wf, obj=0, axis=0)
wf2 = np.delete(wf2, obj=0, axis=0)
plt.figure()
plt.plot(domix, wf)
plt.plot(domix, wf2)
plt.quiver(x, z, Vx, Vz)
plt.xlabel("X (m)")
plt.ylabel("Z (m)")
plt.xlim(0, 500)
plt.ylim(-60, 6)
plt.show()
