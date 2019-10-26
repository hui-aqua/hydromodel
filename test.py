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

print(1.2 * np.ones((10, 1)))
D = 50.0  # [m]  fish cage diameter
H = 30.0  # [m]  fish cage height
# L = 1.5  # [m]  bar length
NT = 30  # it can use int(pi*D/L)   # Number of the nodes in circumference
# NT = int(pi * D / L)
NN = 20  # it can use int(H/L)      # Number-1 of the nodes in the height
# NN = int(H / L)
p = []
cagebottomcenter = [0, 0, -H]

# generate the point coordinates matrix for the net
for i in range(0, NT):
    for j in range(0, NN + 1):
        p.append([D / 2 * np.cos(i * 2 * pi / float(NT)), D / 2 * np.sin(i * 2 * pi / float(NT)), -j * H / float(NN)])
p.append(cagebottomcenter)
