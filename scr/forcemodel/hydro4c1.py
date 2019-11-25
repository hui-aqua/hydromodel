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

    def reductionfactorblvin(self, alf):  # alf is the inflow angle
        alf = np.abs(alf)
        refa = (np.cos(alf) + 0.05 - 0.38 * self.Sn) / (np.cos(alf) + 0.05)
        return max(0, refa)


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
    def M1(self, realtimeposi, U):
        # ref is a list of which elements in the wake region
        # ref. J.S. Bessonneau and D. Marichal. 1998 # cd=1.2,ct=0.1.
        num_node = len(self.posi)
        num_line = len(self.hydroelem)
        Ct = 0.1
        Cn = 1.2
        F = np.zeros((num_node, 3))  # force on nodes
        for i in range(num_line):
            Ueff = U
            b = Cal_distence(realtimeposi[int(self.hydroelem[i][0])], realtimeposi[int(self.hydroelem[i][1])])
            a = Cal_orientation(realtimeposi[int(self.hydroelem[i][0])], realtimeposi[int(self.hydroelem[i][1])])
            if i in self.ref:
                Ueff = 0.8 * U
            ft = 0.5 * row * self.dwh * (b - self.dwh) * Ct * pow(np.dot(a, Ueff), 2) * a
            fn = 0.5 * row * self.dwh * (b - self.dwh) * Cn * (
                    Ueff - np.dot(a, Ueff) * a) * np.linalg.norm(
                (Ueff - np.dot(a, Ueff) * a))
            F[int(self.hydroelem[i][0])] = F[int(self.hydroelem[i][0])] + 0.5 * (fn + ft)
            F[int(self.hydroelem[i][1])] = F[int(self.hydroelem[i][1])] + 0.5 * (fn + ft)
        return F

    def M2(self, U):  # constant drag coefficient value 1.3
        num_node = len(self.posi)
        num_line = len(self.hydroelem)
        Ct = 0.1
        Cn = 1.3
        F = np.zeros((num_node, 3))  # force on nodes
        for i in range(num_line):
            Ueff = np.array(U)
            b = Cal_distence(self.posi[int(self.hydroelem[i][0])], self.posi[int(self.hydroelem[i][1])])
            a = Cal_orientation(self.posi[int(self.hydroelem[i][0])], self.posi[int(self.hydroelem[i][1])])
            if i in self.ref:
                Ueff = 0.8 * np.array(U)
            ft = 0.5 * row * self.dwh * (b - self.dwh) * Ct * pow(np.dot(a, Ueff), 2) * a
            fn = 0.5 * row * self.dwh * (b - self.dwh) * Cn * (
                    Ueff - np.dot(a, Ueff) * a) * np.linalg.norm(
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
        self.hydroelems = hydroelems  # the connections of the twines[[p1,p2][p2,p3]]
        self.dwh = dwh  # used for the force calculation (reference area)
        # can be a consistent number or a list
        self.dw0 = dw0  # used for the hydrodynamic coefficients
        # can be a consistent number or a list
        self.Sn = solidity
        self.wake = Net2NetWake(self.posi, self.hydroelems, Udirection, self.Sn)  # create wake object
        self.ref = self.wake.geteleminwake()  # Calculate the element in the wake

    def Save_ref(self):
        return self.ref

    def S1(self, realtimeposi, U):
        # from Aarsnes model(1990) the Sn should be less than 0.35
        # Reynolds number in range from 1400 to 1800
        num_node = len(self.posi)  # the number of the node
        F = np.zeros((num_node, 3))  # force on nodes, initial as zeros
        for panel in self.hydroelems:  # loop based on the hydrodynamic elements
            alpha, surN, surL, surA = Cal_element(panel, realtimeposi,
                                                  U)  # calculate the inflow angel, normal vector, lift force factor, area of the hydrodyanmic element
            # set([int(k) for k in set(panel)])   # get a set of the node sequence in the element
            if self.hydroelems.index(panel) in self.ref:  # if the element in the wake region
                Ueff = U * self.wake.reductionfactorblvin(alpha)  # the effective velocity = U* reduction factor
            else:
                Ueff = U  # if not in the wake region, the effective velocity is the undistrubed velocity

            if len([int(k) for k in set(panel)]) == 3:  # the hydrodynamic element is a triangle
                nodes = [k for k in set([int(k) for k in set(panel)])]  # a list of the node sequence
                # Cd and Cl is calculated according to the formula
                Cd = 0.04 + (-0.04 + self.Sn - 1.24 * pow(self.Sn, 2) +
                             13.7 * pow(self.Sn, 3)) * np.cos(alpha)
                Cl = (0.57 * self.Sn - 3.54 * pow(self.Sn, 2) +
                      10.1 * pow(self.Sn, 3)) * np.sin(2 * alpha)
                # Calculate the drag and lift force
                fd = 0.5 * row * surA * Cd * np.linalg.norm(Ueff) * Ueff
                fl = 0.5 * row * surA * Cl * pow(np.linalg.norm(Ueff), 2) * surL
                # map the force on the corresponding nodes
                F[nodes[0]] = F[nodes[0]] + (fd + fl) / 3
                F[nodes[1]] = F[nodes[1]] + (fd + fl) / 3
                F[nodes[2]] = F[nodes[2]] + (fd + fl) / 3
            else:  # the hydrodynamic element is a square
                for i in range(len(panel)):  # loop 4 times to map the force
                    nodes = [int(k) for k in panel]  # get the list of nodes [p1,p2,p3,p4]
                    nodes.pop(i)  # delete the i node to make the square to a triangle
                    panelInSquare = nodes  # delete the i node to make the square to a triangle
                    alpha, surN, surL, surA = Cal_element(panelInSquare, realtimeposi,
                                                               U)  # calculate the inflow angel, normal vector, lift force factor, area of the hydrodyanmic element
                    Cd = 0.04 + (-0.04 + self.Sn - 1.24 * pow(self.Sn, 2) +
                                 13.7 * pow(self.Sn, 3)) * np.cos(alpha)
                    Cl = (0.57 * self.Sn - 3.54 * pow(self.Sn, 2) +
                          10.1 * pow(self.Sn, 3)) * np.sin(2 * alpha)
                    fd = 0.5 * row * surA * Cd * np.linalg.norm(Ueff) * Ueff
                    fl = 0.5 * row * surA * Cl * pow(np.linalg.norm(Ueff), 2) * surL
                    # map the force on the corresponding nodes
                    F[nodes[0]] = F[nodes[0]] + (fd + fl) / 6
                    F[nodes[1]] = F[nodes[1]] + (fd + fl) / 6
                    F[nodes[2]] = F[nodes[2]] + (fd + fl) / 6
        return F


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


def Cal_element(eachpanel, realtimeposi, origvelo):
    # because the mesh construction, the first two node cannot have same index
    a1 = Cal_orientation(realtimeposi[eachpanel[0]], realtimeposi[eachpanel[1]])
    a2 = Cal_orientation(realtimeposi[eachpanel[0]], realtimeposi[eachpanel[2]])
    ba1 = Cal_distence(realtimeposi[eachpanel[0]], realtimeposi[eachpanel[1]])
    ba2 = Cal_distence(realtimeposi[eachpanel[0]], realtimeposi[eachpanel[2]])
    surN = np.cross(a1, a2) / np.linalg.norm(np.cross(a1, a2))
    surA = 0.5 * np.linalg.norm(np.cross(a1 * ba1, a2 * ba2))
    if np.dot(surN, origvelo) < 0:
        surN = -surN
    surL = np.cross(np.cross(origvelo, surN), origvelo) / \
           np.linalg.norm(np.cross(np.cross(origvelo, surN), origvelo) + 0.000000001)

    cosalpha = abs(np.dot(surN, origvelo) / np.linalg.norm(origvelo))
    alpha = np.arccos(cosalpha)
    return alpha, surN, surL, surA
# Might mot use
#     # if set(elementIndex) == 3:  # only three point for the screen.
#     #     newEIndex = [k for k in set(elementIndex)]  # the new set of element index
#     #     newEIndex.sort()
#     a1 = Cal_orientation(self.posi[newEIndex[0]], self.posi[newEIndex[1]])
#     a2 = Cal_orientation(self.posi[newEIndex[0]], self.posi[newEIndex[1]])
#     ba1 = Cal_distence(self.posi[newEIndex[0]], self.posi[newEIndex[1]])
#     ba2 = Cal_distence(self.posi[newEIndex[0]], self.posi[newEIndex[1]])
#     surN = np.cross(a1, a2) / np.linalg.norm(np.cross(a1, a2))
#     if np.dot(surN, Ueff) < 0:
#         surN = -surN
#     # the normal vector of the net plane in positive with current direction
#     surL = np.cross(np.cross(Ueff, surN), Ueff) / \
#            np.linalg.norm(np.cross(np.cross(Ueff, surN), Ueff) + 0.000000001)
#
#     surA = 0.5 * np.linalg.norm(np.cross(a1 * ba1, a2 * ba2))
#     cosalpha = abs(np.dot(surN, Ueff) / np.linalg.norm(Ueff))
#     sinalpha = np.linalg.norm(np.cross(surN, Ueff)) / np.linalg.norm(Ueff)
#     Cd = 0.04 + (-0.04 + self.Sn - 1.24 * pow(self.Sn, 2) +
#                  13.7 * pow(self.Sn, 3)) * cosalpha
#     Cl = (0.57 * self.Sn - 3.54 * pow(self.Sn, 2) +
#           10.1 * pow(self.Sn, 3)) * 2 * sinalpha * cosalpha
#     wake = Net2NetWake(self.posi, self.hydroelem, U, self.Sn)
#     ref = wake.getpaneslinwake()
#     if i in ref:
#         Ueff = U * wake.reductionfactorblvin(np.arccos(cosalpha))
#     fd = 0.5 * row * surA * Cd * np.linalg.norm(Ueff) * Ueff
#     fl = 0.5 * row * surA * Cl * pow(np.linalg.norm(Ueff), 2) * surL
#     F[newEIndex[0]] = F[newEIndex[0]] + (fd + fl) / 3
#     F[newEIndex[1]] = F[newEIndex[1]] + (fd + fl) / 3
#     F[newEIndex[2]] = F[newEIndex[2]] + (fd + fl) / 3
#
# else:
