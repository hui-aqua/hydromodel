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


A = (-0.04 + Sn - 1.24 * pow(Sn, 2) +
     13.7 * pow(Sn, 3))
print("ratio for s1=", (0.02 * pi + A) / (0.04 + A))
print(0.26 / 0.215)

x = np.linspace(1, 200)
plt.subplot(projection='polar')
plt.scatter(x, x, marker='.')
plt.show()

k = np.linspace(1, 5, 10)
print("the length of k is", len(k))


# class Person:
#     def __init__(self, fname, lname):
#         self.firstname = fname
#         self.lastname = lname
#
#     def printname(self):
#         print(self.firstname, self.lastname)
#     def calculatepi(self,time):
#         k=pi+time
#         return k
#
#
# class student(Person):
#     def calculatepi(self,time):
#         super().calculatepi()
#
# x = Person("John", "Doe")
# x.printname()
# print(x.calculatepi(1))
#
# y=student("py","charm")
# y.printname()
# print(y.calculatepi(2))

def func(x):
    y0 = x + 1
    y1 = x * 3
    y2 = y0 ** 3 / pi
    return y0, y1, y2


e1, e2, e3 = func(15)

D = 2
H = 1.8
Dtip = 2
NT = 10  # it can use int(pi*D/L)   # Number of the nodes in circumference
# NT = int(pi * D / L)
NN = 6
p = []
con = []
sur = []
cagebottomcenter = [0, 0, -Dtip]

for j in range(0, NN + 1):
    for i in range(0, NT):
        p.append([D / 2 * np.cos(i * 2 * pi / float(NT)), D / 2 * np.sin(i * 2 * pi / float(NT)), -j * H / float(NN)])
p.append(cagebottomcenter)

for i in range(1, NT + 1):
    for j in range(0, NN + 1):
        if j == NN:
            con.append([i + j * NT - 1, len(p) - 1])  # add the vertical line into geometry
            if i == NT:
                con.append([i + j * NT - 1, 1 + i + (j - 1) * NT - 1])  # add the horizontal line into geometry
                sur.append([i + j * NT - 1, 1 + i + (j - 1) * NT - 1, len(p) - 1, len(p) - 1])
                # add the cone surface into sur
            else:
                con.append([i + j * NT - 1, 1 + i + j * NT - 1])  # add the horizontal line into geometry
                sur.append([i + j * NT - 1, 1 + i + j * NT - 1, len(p) - 1, len(p) - 1])
                # add the cone surface into sur
        else:
            con.append([i + j * NT - 1, i + (j + 1) * NT - 1])  # add the vertical line into geometry
            if i == NT:
                con.append([i + j * NT - 1, 1 + i + (j - 1) * NT - 1])  # add the horizontal line into geometry
                sur.append([i + j * NT - 1, 1 + i + (j - 1) * NT - 1, i + (j + 1) * NT - 1, 1 + i + j * NT - 1])
                # add the horizontal surface into sur
            else:
                con.append([i + j * NT - 1, 1 + i + j * NT - 1])  # add the horizontal line into geometry
                sur.append([i + j * NT - 1, 1 + i + j * NT - 1, i + (j + 1) * NT - 1, 1 + i + (j + 1) * NT - 1])
                # add the horizontal surface into sur

meshinfo = {
    "horizontalElementLength": float(pi * D / NT),
    "verticalElementLength": float(H / NN),
    "coneElementLength": np.sqrt(pow(Dtip - D, 2) + pow(D / 2.0, 2)),
    "numberOfNodes": len(p),
    "numberOfLines": len(con),
    "numberOfSurfaces": len(sur),
    "netLines": con,
    "netSurfaces": sur,
    "netNodes": p
}

f = open("meshinfomation.txt", "w")
f.write(str(meshinfo))
f.close()

with open('meshinfomation.txt', 'r') as f:
    content = f.read()
    dic = eval(content)
