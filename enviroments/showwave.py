import seacondition as sea
import numpy as np
import matplotlib.pyplot as plt

wave1 = sea.IdeLinwave(2, 25, 60)

print(wave1)
t = 0
posi = np.array((0, 0, 0))
velo = wave1.Get_Velo(posi, t)
print("velocity = ", velo)

# 2D domino
domix = np.linspace(0, 50, 2 * 50 + 1)
domiy = np.linspace(-10, 10, 21)
domiz = np.linspace(0, -50, 0.2 * 50 + 1)
T = 0
wf = np.array((0))
x = []
y = []
z = []
waveV = []
Vx = []
Vz = []
for i in range(len(domix)):
    wf = np.vstack((wf, wave1.Get_Surface(np.array((domix[i], 0, 0)), T)))
    x.append(domix[i])
    y.append(domiy[10])
    z.append(domiz[2])
    posi = np.array((domix[i], domiy[10], domiz[2]))
    print("posit=", posi)
    print("velosity is ", wave1.Get_Velo(posi, T))
    waveV.append(wave1.Get_Velo(posi, T))
wf = np.delete(wf, obj=0, axis=0)
Vx = waveV[:][0]
Vz = waveV[:][2]

plt.figure()
plt.plot(domix, wf)
# plt.quiver(x,z,Vx,Vz)
plt.quiver(39.5, -10, -0.11145754, -0.0612743)

plt.xlabel("X (m)")
plt.ylabel("Z (m)")
plt.xlim(0, 50)
plt.ylim(-60, 6)
plt.show()
