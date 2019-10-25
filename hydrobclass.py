# writer: hui.cheng@uis.no
# This is a rewritten version using Class method

import numpy as np
from numpy import pi

row = 1025  # kg/m3   sea water density
Kinvis = 1.004e-6  # when the water tempreture is 20 degree.
Dynvis = 1.002e-3  # when the water tempreture is 20 degree.
refa = 1  # constant reduction factor
# As a gift for my mother country, China.  2019.9.30


# ###############  blevins ployfitting#################
coe25 = np.array([
    -2.892133401021243500e-01, 6.267135574694910893e-01,
    -7.157409449812776603e-02, -8.320909217614042008e-01,
    7.398392740943907642e-01, -2.683467821216800053e-01,
    1.949719351189289560e-02, 8.249793665980104107e-01
])
coe20 = np.array([
    -1.474349975132451362e+00,
    6.490272947305592233e+00,
    -1.146253302377779626e+01,
    1.016432973554554842e+01,
    -4.699724398373956724e+00,
    1.002973285638476986e+00,
    -8.328579182908107947e-02,
    8.608477553083272449e-01,
])
coe35 = np.array([
    -4.25657,
    18.6974,
    -32.7564,
    28.8642,
    -13.4061,
    3.0472,
    -0.304585,
    0.885381,
])


def reductionfactorblvin(alf, coe):
    refa = 0
    alf = np.abs(alf)
    for i in range(len(coe) - 1):
        refa += coe[i] * pow(abs(alf), 7 - i)
    return refa + 0.825


# ###############  blevins ployfitting#################

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
    return np.transpose(POSI)


def Get_velo(tabreu):  # to get the velocity
    CxT2 = tabreu.EXTR_TABLE()
    VX1 = CxT2.values()['DX']
    VX2 = CxT2.values()['DY']
    VX3 = CxT2.values()['DZ']
    VITE = np.array([VX1, VX2, VX3])
    return np.transpose(VITE)
# ## above is used in Code_Aster#######################################


# auto-hydrodyanmic mesh generator#####
def Cal_connection(POSI, thre):
    elem = []
    for i in range(len(POSI)):
        for j in range(len(POSI)):
            if 0.90 * thre < Cal_distence(POSI[i], POSI[j]) < 1.1 * thre:
                if [j, i] not in elem:
                    elem.append([i, j])
    return elem


def Cal_screen(POSI, elem, are):
    sur = []
    for i in range(len(elem)):
        for j in range(len(elem)):
            twoli = set([elem[i][0], elem[i][1], elem[j][0], elem[j][1]])
            if len(set(twoli)) == 3:
                ele = [k for k in twoli]
                ele.sort()
                a1 = Cal_distence(POSI[ele[0]], POSI[ele[1]])
                a2 = Cal_distence(POSI[ele[0]], POSI[ele[2]])
                a3 = Cal_distence(POSI[ele[1]], POSI[ele[2]])
                s = (a1 + a2 + a3) / 2
                K = np.sqrt(s * (s - a1) * (s - a2) * (s - a3))
                if K > are * 0.9:
                    if ele not in sur:
                        sur.append(ele)
    return sur


def Cal_linecenter(p1, p2):
    px = (p2[0] + p1[0]) / 2.0
    py = (p2[1] + p1[1]) / 2.0
    pz = (p2[2] + p1[2]) / 2.0
    return np.array([px, py, pz])


def Cal_tricenter(p1, p2, p3):
    px = (p3[0] + p2[0] + p1[0]) / 3.0
    py = (p3[1] + p2[1] + p1[1]) / 3.0
    pz = (p3[2] + p2[2] + p1[2]) / 3.0
    return np.array([px, py, pz])


def Cal_distence(p1, p2):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    dz = p2[2] - p1[2]
    return np.sqrt(dx**2 + dy**2 + dz**2)


def Cal_orientation(p1, p2):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    dz = p2[2] - p1[2]
    p = np.array([dx, dy, dz])
    return p / np.linalg.norm(p)

# >>>>>>>>>>>>>>>>>>>>>next section>>>>>>>>>>>>>>>>>>>>>
# The following is shielding effect
# >>>>>>>>>>>>>>>>>>>>hui.cheng@uis.no>>>>>>>31.03.2019>
# >>>>>>>>>>>>>>>>>>>>update>>>>>>>>>>>>>>>>>03.04.2019>
def Cal_shie_screen_elem(POSI, elem, U):
    elem_shie = []
    for i in range(len(elem)):
        if np.dot(
                Cal_tricenter(
                    POSI[elem[i][0]],
                    POSI[elem[i][1]],
                    POSI[elem[i][2]],
                ), U) > 0:
            elem_shie.append(i)
    return elem_shie


def Cal_shie_line_elem(POSI, elem, U):
    elem_shie = []
    for i in range(len(elem)):
        if np.dot(Cal_linecenter(
                POSI[elem[i][0]],
                POSI[elem[i][1]],
        ), U) > 0:
            elem_shie.append(i)
# this means the line element center is in the back part of the netcage
    return elem_shie

class HydroMorison:
    """
    For Morison hydrodyanmic models, the code needs the nodes' potions \n
    and the connetions.  \n
    Thus, the input variable is the matrix of nodes and the connetions. \n 
    In addition, the solidity and constant flow reduction are also needed. 
    """

    def __init__(self,posi,con,dwh,dw0):
        self.posi=posi  # the position matrix [[x1,y1,z1][x2,y2,z2]]
        self.line=con   # the connections of the twines[[p1,p2][p2,p3]]
        self.dwh=dwh # used for the force calculation (reference area)
        # can be a consistent number or a list
        self.dw0=dw0    # used for the hydrodynamic coefficients
        # can be a consistent number or a list
    def M1(self,U,Sn,ref):
        # ref is a list of which elements in the wake region
        # ref. J.S. Bessonneau and D. Marichal. 1998 # cd=1.2,ct=0.1.
        num_node = len(self.posi)
        num_line = len(self.line)
        if len(self.dwh)==1:
            self.dwh=self.dwh*np.ones((num_line,1))
        if len(self.dw0)==1:
            self.dw0=self.dw0*np.ones((num_line,1))
        ## if the dwh is not a list, define a list witht a consistent value
        Ct = 0.1
        Cn = 1.2
        a = []  # oriention for the cable
        b = []  # cable length
        F = np.zeros((num_node, 3))  # force on nodes
        for i in range(num_line):
            Ueff = U
            b = Cal_distence(self.posi[self.line[i][0]], self.posi[self.line[i][1]])
            a = Cal_orientation(self.posi[self.line[i][0]], self.posi[self.line[i][1]])
            if i in ref:
                Ueff = 0.8 * U
            ft = 0.5 * row * self.dwh[i] * (b - self.dwh[i]) * Ct * pow(np.dot(a, Ueff),2) * a
            fn = 0.5 * row * self.dwh[i] * (b - self.dwh[i]) * Cn * (
                Ueff - np.dot(a, Ueff) * a) * np.linalg.norm(
                    (Ueff - np.dot(a, Ueff) * a))
            F[int(self.line[i][0])] = F[int(self.line[i][0])] + 0.5 * (fn + ft)
            F[int(self.line[i][1])] = F[int(self.line[i][1])] + 0.5 * (fn + ft)
        return F

    def M2(self,U,ref):
        # ref. Tsutomu Takagi 2003
        # cd=f(re), # ct=0.1. 
        Ct = 0.1 
        print(self.posi)
        num_node = len(self.posi)
        num_line = len(self.line)
        if len(self.dwh)==1:
            self.dwh=self.dwh*np.ones((num_line,1))
        if len(self.dw0)==1:
            self.dw0=self.dw0*np.ones((num_line,1))
        a = []  # oriention for the cable
        b = []  # cable length
        F = np.zeros((num_node, 3))  # force on nodes
        for i in range(num_line):
            Ueff = U
            Re = np.linalg.norm(Ueff) * self.dw0[i] / Kinvis
            if Re < 200:
                Cn = pow(10, 0.7) * pow(Re, 0.3)
            else:
                Cn = 1.2
            b = Cal_distence(self.posi[self.line[i][0]], self.posi[self.line[i][1]])
            a = Cal_orientation(self.posi[self.line[i][0]], self.posi[self.line[i][1]])
            if i in ref:
                Ueff = 0.8 * U
            ft = 0.5 * row * self.dwh[i] * (b - self.dwh[i]) * Ct * pow(np.dot(a, Ueff),
                                                              2) * a
            fn = 0.5 * row * self.dwh[i] * (b - self.dwh[i]) * Cn * (
                Ueff - np.dot(a, Ueff) * a) * np.linalg.norm(
                    (Ueff - np.dot(a, Ueff) * a))
            F[int(self.line[i][0])] = F[int(self.line[i][0])] + 0.5 * (fn + ft)
            F[int(self.line[i][1])] = F[int(self.line[i][1])] + 0.5 * (fn + ft)
        return F

    def M4(self,U,ref):
        # ref. yunpeng zhao 2003
        # cd=f(ren), # ct=f(ren).  # cm=1.0
        num_node = len(self.posi)
        num_line = len(self.line)
        if len(self.dwh)==1:
            self.dwh=self.dwh*np.ones((num_line,1))
        if len(self.dw0)==1:
            self.dw0=self.dw0*np.ones((num_line,1))
        a = []  # oriention for the cable
        b = []  # cable length
        F = np.zeros((num_node, 3))  # force on nodes
        for i in range(num_line):
            if i in ref:
                Ueff = 0.8 * U
            else:
                Ueff = U
            b = Cal_distence(self.posi[self.line[i][0]], self.posi[self.line[i][1]])
            a = Cal_orientation(self.posi[self.line[i][0]], self.posi[self.line[i][1]])
            ren = row *self.dw0 * np.linalg.norm(
                (Ueff - np.dot(a, Ueff) * a)) / Dynvis
            Ct = pi * Dynvis * (0.55 * np.sqrt(ren) + 0.084 * pow(ren, 2.0 / 3.0))
            s = -0.07721565 + np.log(8.0 / ren)
            if ren < 1:
                Cn = 8 * pi * (1 - 0.87 * pow(s, -2)) / (s * ren)
            elif ren < 30:
                Cn = 1.45 + 8.55 * pow(ren, -0.9)
            else:
                Cn = 1.1 + 4 * pow(ren, -0.5)
            ft = 0.5 * row * self.dwh[i] * (b - self.dwh[i]) * Ct * pow(np.dot(a, Ueff),
                                                              2) * a
            fn = 0.5 * row * self.dwh[i] * (b - self.dwh[i]) * Cn * (
                Ueff - np.dot(a, Ueff) * a) * np.linalg.norm(
                    (Ueff - np.dot(a, Ueff) * a))
            F[int(self.line[i][0])] = F[int(self.line[i][0])] + 0.5 * (fn + ft)
            F[int(self.line[i][1])] = F[int(self.line[i][1])] + 0.5 * (fn + ft)
        return F