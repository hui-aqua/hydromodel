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
meshinfo = {
    "horizontal element length": float(11),
    "vertical element length": float(34),
    "cone element length": np.sqrt(34),
    "number of nodes": 123,
    "number of lines": 21,
    "number of surfaces": 12
}
import pickle

f = open("file.pkl", "wb")
pickle.dump(meshinfo, f)
f.close()

pkl_file = open('file.pkl', 'rb')
meshinfo2 = pickle.load(pkl_file)
pkl_file.close()

f = open("dict.txt", "w")
f.write(str(meshinfo))
f.close()
