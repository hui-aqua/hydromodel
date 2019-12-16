"""
A module can be used to calculate the hydrodynamic forces on nets in Code_Aster.
To use this module, one should be import this into the input file for calculations.
Any questions about this code, please email: hui.cheng@uis.no
"""
import numpy as np

row = 1025  # kg/m3   sea water density
Kinvis = 1.004e-6  # when the water temperature is 20 degree.
Dynvis = 1.002e-3  # when the water temperature is 20 degree.


class Net2NetWake:
    def __init__(self, posi, hydroelement, U, Sn):
        self.posi = posi  # a list of all the nodes for net
        self.hydroelement = hydroelement  # a list of all the elements for net
        self.U = U  # incoming velocity for cage
        self.cagecenter = np.array([0, 0, 0])  # set the cage center is [0,0,0]
        self.Sn = Sn

    def geteleminwake(self):
        elem_shie = []
        for i in range(len(self.hydroelement)):
            for j in range(len(self.hydroelement[i])):
                x = 0
                y = 0
                z = 0
                x += self.posi[self.hydroelement[i][j]][0] / len(self.hydroelement[i])
                y += self.posi[self.hydroelement[i][j]][1] / len(self.hydroelement[i])
                z += self.posi[self.hydroelement[i][j]][2] / len(self.hydroelement[i])
            vectortocagecenter = (np.array([x, y, z]) - self.cagecenter)
            if np.dot(vectortocagecenter, self.U) < 0:
                elem_shie.append(i)
        return elem_shie

    def reductionfactor2(self, alf):  # alf is the inflow angle
        alf = np.abs(alf)
        refa = (np.cos(alf) + 0.05 - 0.38 * self.Sn) / (np.cos(alf) + 0.05)
        return max(0, refa)

    def reductionfactor1(self, Sn):  # alf is the inflow angle
        cd = 0.04 + (-0.04 + 0.33 * self.Sn + 6.54 * pow(self.Sn, 2) - 4.88 * pow(self.Sn, 3))
        return 1 - 0.46 * cd


class HydroMorison:
    """
    For Morison hydrodynamic models, the code needs the nodes' potions \n
    and the connections.  \n
    Thus, the input variable is the matrix of nodes and the connections. \n
    In addition, the solidity and constant flow reduction are also needed.
    """

    def __init__(self, posimatrix, hydroelem, solidity, Udirection, dwh=0.0, dw0=0.0):
        self.posi = posimatrix  # the position matrix [[x1,y1,z1][x2,y2,z2]]
        self.hydroelem = hydroelem  # the connections of the twines[[p1,p2][p2,p3]]
        self.dwh = dwh  # used for the force calculation (reference area)
        # can be a consistent number or a list
        self.dw0 = dw0  # used for the hydrodynamic coefficients
        # can be a consistent number or a list
        self.Sn = solidity
        wake = Net2NetWake(self.posi, self.hydroelem, Udirection, self.Sn)
        self.ref = wake.geteleminwake()

    def Save_ref(self):
        return self.ref

    def M1(self):
        return 1.2, 0.1

    def M2(self):
        return 1.3, 0.0

    def M3(self, U):
        Re = row * self.dw0 * np.linalg.norm(U) / Dynvis
        if Re < 200:
            Cn = pow(10, 0.7) * pow(Re, -0.3)
        else:
            Cn = 1.2
        return Cn, 0.1

    def M4(self, U):
        Re = row * self.dw0 * np.linalg.norm(U) / Dynvis
        Ct = np.pi * Dynvis * (0.55 * np.sqrt(Re) + 0.084 * pow(Re, 2.0 / 3.0))
        s = -0.07721565 + np.log(8.0 / Re)
        if Re < 1:
            Cn = 8 * np.pi * (1 - 0.87 * pow(s, -2)) / (s * Re)
        elif Re < 30:
            Cn = 1.45 + 8.55 * pow(Re, -0.9)

        else:
            Cn = 1.1 + 4 * pow(Re, -0.5)
        return Cn, Ct

    def M5(self, U):
        Re = row * self.dw0 * np.linalg.norm(U) / Dynvis
        Cn = -3.2891e-5 * pow(Re * self.Sn * self.Sn, 2) + 0.00068 * Re * pow(self.Sn, 2) + 1.4253
        return Cn, 0

    def TwineForce(self, realtimeposi, U):
        # ref is a list of which elements in the wake region
        # ref. J.S. Bessonneau and D. Marichal. 1998 # cd=1.2,ct=0.1.
        num_node = len(self.posi)
        num_line = len(self.hydroelem)
        F = np.zeros((num_node, 3))  # force on nodes
        for i in range(num_line):
            b = Cal_distence(realtimeposi[int(self.hydroelem[i][0])], realtimeposi[int(self.hydroelem[i][1])])
            a = Cal_orientation(realtimeposi[int(self.hydroelem[i][0])], realtimeposi[int(self.hydroelem[i][1])])
            if i in self.ref:
                Ueff = 0.8 * np.array(U)
            else:
                Ueff = np.array(U)
            Cn, Ct = self.M1()
            # Cn, Ct = self.M5(Ueff) if M5 is applied
            ft = 0.5 * row * self.dwh * (b - self.dwh) * Ct * np.dot(a, Ueff) * a * np.linalg.norm(np.dot(a, Ueff))
            fn = 0.5 * row * self.dwh * (b - self.dwh) * Cn * (Ueff - np.dot(a, Ueff) * a) * np.linalg.norm(
                (Ueff - np.dot(a, Ueff) * a))
            F[int(self.hydroelem[i][0])] = F[int(self.hydroelem[i][0])] + 0.5 * (fn + ft)
            F[int(self.hydroelem[i][1])] = F[int(self.hydroelem[i][1])] + 0.5 * (fn + ft)
        return F


class HydroScreen:
    """
    For Screen hydrodynamic models, the code needs the panel' potions \n
    and the connections.  \n
    Thus, the input variable is the matrix of nodes and the connetions. \n
    In addition, the solidity and constant flow reduction are also needed.
    """

    def __init__(self, posiMatrix, hydroelems, solidity, Udirection, dwh=0.0, dw0=0.0):
        self.posi = posiMatrix  # the position matrix [[x1,y1,z1][x2,y2,z2]]
        self.hydroelems = self.ConhydroE(hydroelems)  # the connections of the twines[[p1,p2][p2,p3]]
        self.dwh = dwh  # used for the force calculation (reference area)
        # can be a consistent number or a list
        self.dw0 = dw0  # used for the hydrodynamic coefficients
        # can be a consistent number or a list
        self.Sn = solidity  # solidity of th net
        self.wake = Net2NetWake(self.posi, self.hydroelems, Udirection, self.Sn)  # create wake object
        self.ref = self.wake.geteleminwake()  # get the elements in the wake

    def Save_ref(self):
        # return the index of the elements in the wake region
        return self.ref

    def Save_hydroelems(self):
        # return the index of the elements in the wake region
        return self.hydroelems

    def ConhydroE(self, hydroE):
        newHydroE = []
        for panel in hydroE:  # loop based on the hydrodynamic elements
            if len([int(k) for k in set(panel)]) == 3:  # the hydrodynamic element is a triangle
                newHydroE.append([k for k in set([int(k) for k in set(panel)])])  # a list of the node sequence
            else:
                for i in range(len(panel)):  # loop 4 times to map the force
                    nodes = [int(k) for k in panel]  # get the list of nodes [p1,p2,p3,p4]
                    nodes.pop(i)  # delete the i node to make the square to a triangle
                    newHydroE.append(nodes)  # delete the i node to make the square to a triangle
        return newHydroE

    def S1(self, inflowAngle):
        Cd = 0.04 + (-0.04 + self.Sn - 1.24 * pow(self.Sn, 2) + 13.7 * pow(self.Sn, 3)) * np.cos(inflowAngle)
        Cl = (0.57 * self.Sn - 3.54 * pow(self.Sn, 2) + 10.1 * pow(self.Sn, 3)) * np.sin(2 * inflowAngle)
        return Cd, Cl

    def S2(self, inflowAngle):
        Cd = 0.04 + (-0.04 + 0.33 * self.Sn + 6.54 * pow(self.Sn, 2) - 4.88 * pow(self.Sn, 3)) * np.cos(inflowAngle)
        Cl = (-0.05 * self.Sn - 2.3 * pow(self.Sn, 2) - 1.76 * pow(self.Sn, 3)) * np.sin(2 * inflowAngle)
        return Cd, Cl

    def S3(self, inflowAngle, a1, a3, b2, b4, U):
        Re = row * self.dw0 * np.linalg.norm(U) / Dynvis / (1 - self.Sn)  # Re
        cdcyl = -78.46675 + 254.73873 * np.log10(Re) - 327.8864 * pow(np.log10(Re), 2) + 223.64577 * pow(np.log10(Re),
                                                                                                         3) - 87.92234 * pow(
            np.log10(Re), 4) + 20.00769 * pow(np.log10(Re), 5) - 2.44894 * pow(np.log10(Re), 6) + 0.12479 * pow(
            np.log10(Re), 7)
        Cd0 = cdcyl * (self.Sn * (2 - self.Sn)) / (2.0 * pow((1 - self.Sn), 2))
        Cl0 = np.pi * cdcyl * self.Sn / pow(1 - self.Sn, 2) / (8 + cdcyl * self.Sn / pow(1 - self.Sn, 2))
        Cd = Cd0 * (a1 * np.cos(inflowAngle) + a3 * np.cos(3 * inflowAngle))
        Cl = Cl0 * (b2 * np.sin(2 * inflowAngle) + b4 * np.sin(4 * inflowAngle))
        return Cd, Cl

    def S4(self, inflowAngle, U):
        Re = np.linalg.norm(U) * self.dw0 * row / Dynvis
        Rey = Re / (2 * self.Sn)
        Ct = 0.1 * pow(Re, 0.14) * self.Sn
        Cn = 3 * pow(Rey, -0.07) * self.Sn
        Cd = Cn * np.cos(inflowAngle) * pow(np.cos(inflowAngle), 2) + Ct * np.sin(inflowAngle) * pow(
            np.sin(inflowAngle), 2)
        Cl = Cn * np.sin(inflowAngle) * pow(np.cos(inflowAngle), 2) + Ct * np.cos(inflowAngle) * pow(
            np.sin(inflowAngle), 2)
        return Cd, Cl

    def S5(self, inflowAngle):
        # polynomial fitting
        Cd = 0.556 * pow(inflowAngle, 7) - 1.435 * pow(inflowAngle, 6) - 2.403 * pow(
            inflowAngle, 5) + 11.75 * pow(inflowAngle, 4) - 13.48 * pow(inflowAngle, 3) + 5.079 * pow(
            inflowAngle, 2) - 0.9431 * pow(inflowAngle, 1) + 1.155
        Cl = -10.22 * pow(inflowAngle, 9) + 69.22 * pow(inflowAngle, 8) - 187.9 * pow(
            inflowAngle, 7) + 257.3 * pow(inflowAngle, 6) - 181.6 * pow(inflowAngle, 5) + 59.14 * pow(
            inflowAngle, 4) - 7.97 * pow(inflowAngle, 3) + 2.103 * pow(
            inflowAngle, 2) + 0.2325 * pow(inflowAngle, 1) + 0.01294
        return Cd, Cl

    def S6(self, inflowAngle, U, knot):
        Re_cyl = row * self.dw0 * np.linalg.norm(U) / Dynvis / (1 - self.Sn) + 0.000001
        cdcyl = 1 + 10.0 / (pow(Re_cyl, 2.0 / 3.0))
        Cd = cdcyl * (0.12 - 0.74 * self.Sn + 8.03 * pow(self.Sn, 2)) * pow(inflowAngle, 3)
        if knot == 'knotless':
            return Cd, 0
        elif knot == 'knotted':
            meshsize = 10 * self.dw0  # assume Sn=0.2
            D = 2 * self.dw0  # assume the knot is twice of the diameter of the twine
            Re_sp = row * D * np.linalg.norm(U) / Dynvis / (1 - self.Sn) + 0.000001
            cdsp = 24.0 / Re_sp + 6.0 / (1 + np.sqrt(Re_sp)) + 0.4
            Cd = (cdcyl * 8 * pow(D, 2) + cdsp * np.pi * meshsize * self.dw0) / np.pi * meshsize * self.dw0 * (
                    0.12 - 0.74 * self.Sn + 8.03 * pow(self.Sn, 2)) * pow(inflowAngle, 3)
            return Cd, 0
        else:
            pass

    def ScreenForce(self, realTimePositions, U):
        num_node = len(self.posi)  # the number of the node
        hydroForces_nodes = np.zeros((num_node, 3))  # force on nodes, initial as zeros
        for panel in self.hydroelems:  # loop based on the hydrodynamic elements
            alpha, surN, surL, surA = Cal_element(panel, realTimePositions, U)
            # calculate the inflow angel, normal vector, lift force factor, area of the hydrodynamic element
            # set([int(k) for k in set(panel)])   # get a set of the node sequence in the element
            if self.hydroelems.index(panel) in self.ref:  # if the element in the wake region
                Ueff = U * self.wake.reductionfactor2(alpha)  # the effective velocity = U* reduction factor
            else:
                Ueff = U  # if not in the wake region, the effective velocity is the undisturbed velocity
            Cd, Cl = self.S1(alpha)
            fd = 0.5 * row * surA * Cd * np.linalg.norm(Ueff) * Ueff
            fl = 0.5 * row * surA * Cl * pow(np.linalg.norm(Ueff), 2) * surL
            # map the force on the corresponding nodes
            hydroForces_nodes[panel[0]] = hydroForces_nodes[panel[0]] + (fd + fl) / 6
            hydroForces_nodes[panel[1]] = hydroForces_nodes[panel[1]] + (fd + fl) / 6
            hydroForces_nodes[panel[2]] = hydroForces_nodes[panel[2]] + (fd + fl) / 6
        return hydroForces_nodes

    def screenFsi(self, realTimePositions, U):
        hydroForce_elements = []  # force on netpanel, initial as zeros
        for panel in self.hydroelems:  # loop based on the hydrodynamic elements
            alpha, surN, surL, surA = Cal_element(panel, realTimePositions, U[self.hydroelems.index(panel)])
            Cd, Cl = self.S1(alpha)
            fd = 0.5 * row * surA * Cd * np.linalg.norm(U[self.hydroelems.index(panel)]) * U[
                self.hydroelems.index(panel)]
            fl = 0.5 * row * surA * Cl * pow(np.linalg.norm(U[self.hydroelems.index(panel)]), 2) * surL
            hydroForce_elements.append((fd + fl) / 2.0)
        return hydroForce_elements


# four functions used in the current file

def Cal_distence(p1, p2):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    dz = p2[2] - p1[2]
    return np.sqrt(dx ** 2 + dy ** 2 + dz ** 2)


def Cal_orientation(p1, p2):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    dz = p2[2] - p1[2]
    p = np.array([dx, dy, dz])
    return p / np.linalg.norm(p)


# two function used by code_aster
# ## to get the position ##########################################
def Get_posi(tabreu):
    CxT = tabreu.EXTR_TABLE()
    COOR1 = CxT.values()['COOR_X']
    COOR2 = CxT.values()['COOR_Y']
    COOR3 = CxT.values()['COOR_Z']
    DX1 = CxT.values()['DX']
    DX2 = CxT.values()['DY']
    DX3 = CxT.values()['DZ']
    POSI = np.array([COOR1, COOR2, COOR3]) + np.array([DX1, DX2, DX3])
    # print('posi is'+str(np.transpose(POSI)))
    return np.transpose(POSI)


def Get_velo(tabreu):  # to get the velocity
    CxT2 = tabreu.EXTR_TABLE()
    VX1 = CxT2.values()['DX']
    VX2 = CxT2.values()['DY']
    VX3 = CxT2.values()['DZ']
    VITE = np.array([VX1, VX2, VX3])
    return np.transpose(VITE)


def Cal_element(eachpanel, realTimePositions, origvelo):
    # because the mesh construction, the first two node cannot have same index
    a1 = Cal_orientation(realTimePositions[eachpanel[0]], realTimePositions[eachpanel[1]])
    a2 = Cal_orientation(realTimePositions[eachpanel[0]], realTimePositions[eachpanel[2]])
    ba1 = Cal_distence(realTimePositions[eachpanel[0]], realTimePositions[eachpanel[1]])
    ba2 = Cal_distence(realTimePositions[eachpanel[0]], realTimePositions[eachpanel[2]])
    surN = np.cross(a1, a2) / np.linalg.norm(np.cross(a1, a2))
    surA = 0.5 * np.linalg.norm(np.cross(a1 * ba1, a2 * ba2))
    if np.dot(surN, origvelo) < 0:
        surN = -surN
    surL = np.cross(np.cross(origvelo, surN), origvelo) / \
           np.linalg.norm(np.cross(np.cross(origvelo, surN), origvelo) + 0.000000001)

    cosalpha = abs(np.dot(surN, origvelo) / np.linalg.norm(origvelo))
    alpha = np.arccos(cosalpha)
    return alpha, surN, surL, surA
