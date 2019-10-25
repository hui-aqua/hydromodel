# writer: hui.cheng@uis.no
import numpy as np
from numpy import pi

# here is hydrodynamic parameter need to defined first
dwhydro = 0.0
# [m]  hydrodynamic twine diameter, it must define in the comm file
# dwhyo is used to get the force coefficients for the twine
dwmesh = 0.0
# [m] twine diameter for the force. Usually,
# dwmesh is larger than dwhydro because of mesh grouping.
# dwmesh is used to calculated the projected area and forces.
# it must define in the comm file
row = 1025  # kg/m3   sea water density
Kinvis = 1.004e-6  # when the water tempreture is 20 degree.
Dynvis = 1.002e-3  # when the water tempreture is 20 degree.
refa = 1  # constant reduction factor


# >>> revise 06.05.2019. change the b --> b-dwhyo. to
#    to reduce the calculation overlaping on the knot.

class Net2NetWake:
    def __init__(self, posi, hydroelement, U, cagecenter):
        self.posi = []
        self.hydroelement = []
        self.U = []
        self.cagecenter = np.zeros((3, 1))
        self.elem_shie=[]

    def getpaneslinwake(self, posi, hydroelement, U):
        elem_shie = []
        for i in range(len(self.hydroelement)):
            elmentcenter = Cal_tricenter(self.posi[self.hydroelement[i][0]],
                                          self.posi[self.hydroelement[i][1]],
                                          self.posi[self.hydroelement[i][2]])
            vectortocagecenter = (elmentcenter - self.cagecenter)
            if np.dot(vectortocagecenter, U) < 0:
                elem_shie.append(i)
        return self.elem_shie

    def getlinesinwake(self, posi, hydroelement, U):
        elem_shie = []
        for i in range(len(self.hydroelement)):
            elmentcenter = Cal_linecenter(
                self.posi[int(self.hydroelement[i][0])],
                self.posi[int(self.hydroelement[i][1])])
            vectortocagecenter = (elmentcenter - self.cagecenter)
            if np.dot(vectortocagecenter, U) < 0:
                elem_shie.append(i)
        return self.elem_shie


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


# the line element is generate by meshcreator
# This function is not used anymore
# def Cal_connection(POSI, thre):
#     elem = []
#     for i in range(len(POSI)):
#         for j in range(len(POSI)):
#             if 0.90 * thre < Cal_distence(POSI[i], POSI[j]) < 1.1 * thre:
#                 if [j, i] not in elem:
#                     elem.append([i, j])
#     return elem


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
    return np.sqrt(dx ** 2 + dy ** 2 + dz ** 2)


def Cal_orientation(p1, p2):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    dz = p2[2] - p1[2]
    p = np.array([dx, dy, dz])
    # print(p)
    return p / np.linalg.norm(p)


def Get_Velo_line(wave, POSI, LINE, T):
    num_line = len(LINE)
    WaveVelo = np.zeros((num_line, 3))
    for i in range(num_line):
        linecenter = Cal_linecenter(POSI[int(LINE[i][0])], POSI[int(LINE[i][1])])
        linecenter[2] = linecenter[2] - 60
        WaveVelo[i, :] = wave.Get_Velo(linecenter, T)
    return WaveVelo


def Cal_FM1(POSI, LINE, U, Sn, ref):
    # ref. J.S. Bessonneau and D. Marichal. 1998
    # cd=1.2,ct=0.1.
    # cm=1.0
    # here in the pure current condition, the cm is useless.
    num_node = len(POSI)
    Ct = 0.1
    Cn = 1.2
    a = []  # oriention for the cable
    b = []  # cable length
    F = np.zeros((num_node, 3))  # force on nodes
    for i in range(len(LINE)):
        Ueff = U
        b = Cal_distence(POSI[int(LINE[i][0])], POSI[int(LINE[i][1])])
        if 1.4 < b < 1.6:
            dwmeshc = dwmesh
        elif 2.8 < b < 3.0:
            dwmeshc = dwmesh
        else:
            dwmeshc = dwmesh * 5.7 / 1.5
        a = Cal_orientation(POSI[int(LINE[i][0])], POSI[int(LINE[i][1])])
        if i in ref:
            Ueff = 0.8 * (U)
        ft = 0.5 * row * dwmeshc * (b - dwmeshc) * Ct * pow(np.dot(a, Ueff),2) * a
        fn = 0.5 * row * dwmeshc * (b - dwmeshc) * Cn * (
                Ueff - np.dot(a, Ueff) * a) * np.linalg.norm(
            (Ueff - np.dot(a, Ueff) * a))
        F[int(LINE[i][0])] = F[int(LINE[i][0])] + 0.5 * fn + 0.5 * ft
        F[int(LINE[i][1])] = F[int(LINE[i][1])] + 0.5 * fn + 0.5 * ft

    return F


def Cal_FM2(POSI, LINE, U, Wave, Sn, ref):
    # ref. Tsutomu Takagi 2003
    # cd=f(re),
    # ct=0.1.
    # cm=1.0
    # here in the pure current condition, the cm is useless.
    num_node = len(POSI)
    Ct = 0.1
    # Cn = 1.2
    a = []  # oriention for the cable
    b = []  # cable length
    F = np.zeros((num_node, 3))  # force on nodes
    for i in range(len(LINE)):
        Ueff = U + Wave[i]
        Re = np.linalg.norm(Ueff) * dwhydro / Kinvis
        if Re < 200:
            Cn = pow(10, 0.7) * pow(Re, 0.3)
        else:
            Cn = 1.2
        b = Cal_distence(POSI[int(LINE[i][0])], POSI[int(LINE[i][1])])
        a = Cal_orientation(POSI[int(LINE[i][0])], POSI[int(LINE[i][1])])
        if i in ref:
            Ueff = 0.8 * (U + Wave[i])
        ft = 0.5 * row * dwmesh * (b - dwmesh) * Ct * pow(np.dot(a, Ueff),
                                                          2) * a
        fn = 0.5 * row * dwmesh * (b - dwmesh) * Cn * (
                Ueff - np.dot(a, Ueff) * a) * np.linalg.norm(
            (Ueff - np.dot(a, Ueff) * a))
        F[int(LINE[i][0])] = F[int(LINE[i][0])] + 0.5 * fn + 0.5 * ft
        F[int(LINE[i][1])] = F[int(LINE[i][1])] + 0.5 * fn + 0.5 * ft
    return F


def Cal_FM3(POSI, LINE, U, Sn, ref):
    # '''
    # This method comes from Rong wan, which has been used for a long time in
    # OUC,
    # but it can not be used in the wave envirioment, because it did not
    # include the tranfromation of coordainate.
    # '''
    row = 1025  # kg/m3  sea water density
    num_node = len(POSI)
    a = []  # oriention for the cable
    b = []  # cable length
    F = np.zeros((num_node, 3))  # force on nodes
    for i in range(len(LINE)):
        if i in ref:
            Ueff = 0.8 * U
        else:
            Ueff = U
        b = Cal_distence(POSI[int(LINE[i][0])], POSI[int(LINE[i][1])])
        a = Cal_orientation(POSI[int(LINE[i][0])], POSI[int(LINE[i][1])])

        Cx = 1.3 * (1 - pow(a[0], 2))
        if np.abs(a[1]) == 1 or np.abs(a[2]) == 1:
            Cy = 0
            Cz = 0
        else:
            Cy = -1.3 * a[0] * a[1] * np.abs(a[1]) / np.sqrt(1 - a[2] ** 2)
            Cz = -1.3 * a[0] * a[2] * np.abs(a[2]) / np.sqrt(1 - a[1] ** 2)
        F[int(LINE[i][0])][0] = F[int(LINE[i][0])][0] + 0.5 * Cx * (b - dwmesh) * dwmesh * row * np.linalg.norm(
            Ueff) ** 2
        F[int(LINE[i][0])][1] = F[int(LINE[i][0])][1] + 0.5 * Cy * (b - dwmesh) * dwmesh * row * np.linalg.norm(
            Ueff) ** 2
        F[int(LINE[i][0])][2] = F[int(LINE[i][0])][2] + 0.5 * Cz * (b - dwmesh) * dwmesh * row * np.linalg.norm(
            Ueff) ** 2
        F[int(LINE[i][1])][0] = F[int(LINE[i][1])][0] + 0.5 * Cx * (b - dwmesh) * dwmesh * row * np.linalg.norm(
            Ueff) ** 2
        F[int(LINE[i][1])][1] = F[int(LINE[i][1])][1] + 0.5 * Cy * (b - dwmesh) * dwmesh * row * np.linalg.norm(
            Ueff) ** 2
        F[int(LINE[i][1])][2] = F[int(LINE[i][1])][2] + 0.5 * Cz * (b - dwmesh) * dwmesh * row * np.linalg.norm(
            Ueff) ** 2
    return 0.5 * F


def Cal_FM4(POSI, LINE, U, Sn, ref):
    # ref. yunpeng zhao 2003
    # cd=f(ren), # ct=f(ren).  # cm=1.0
    # here in the pure current condition, the cm is useless.
    num_node = len(POSI)
    a = []  # oriention for the cable
    b = []  # cable length
    F = np.zeros((num_node, 3))  # force on nodes
    # print('the sizeof F is >>>>>>>>>>>>>>>>>>', len(F))
    # print('the sizeof line is >>>>>>>>>>>>>>>>>>', len(LINE))
    # print('the sizeof ref is >>>>>>>>>>>>>>>>>>', len(ref))
    print('Here I am in FM4, the dwhydro and dwmesh is  ....\n\n\n' + str([dwhydro, dwmesh]))
    for i in range(len(LINE)):
        if i in ref:
            Ueff = 0.8 * U
        else:
            Ueff = U
        b = Cal_distence(POSI[int(LINE[i][0])], POSI[int(LINE[i][1])])
        a = Cal_orientation(POSI[int(LINE[i][0])], POSI[int(LINE[i][1])])

        ren = row * dwhydro * np.linalg.norm(
            (Ueff - np.dot(a, Ueff) * a)) / Dynvis
        Ct = pi * Dynvis * (0.55 * np.sqrt(ren) + 0.084 * pow(ren, 2.0 / 3.0))
        s = -0.07721565 + np.log(8.0 / ren)
        if ren < 1:
            Cn = 8 * pi * (1 - 0.87 * pow(s, -2)) / (s * ren)
        elif ren < 30:
            Cn = 1.45 + 8.55 * pow(ren, -0.9)

        else:
            Cn = 1.1 + 4 * pow(ren, -0.5)
        ft = 0.5 * row * dwmesh * (b - dwmesh) * Ct * pow(np.dot(a, Ueff),
                                                          2) * a
        fn = 0.5 * row * dwmesh * (b - dwmesh) * Cn * (
                Ueff - np.dot(a, Ueff) * a) * np.linalg.norm(
            (Ueff - np.dot(a, Ueff) * a))
        F[int(LINE[i][0])] = F[int(LINE[i][0])] + 0.5 * fn + 0.5 * ft
        F[int(LINE[i][1])] = F[int(LINE[i][1])] + 0.5 * fn + 0.5 * ft
    return F


def Cal_FM5(POSI, LINE, U, Sn, ref):
    # ref. Cifuntes,c 2017
    # # # cd=f(ren)
    # here in the pure current condition, the cm is useless.
    num_node = len(POSI)
    a = []  # orientation for the cable
    b = []  # cable length
    F = np.zeros((num_node, 3))  # force on nodes
    for i in range(len(LINE)):
        if i in ref:
            Ueff = 0.8 * U
        else:
            Ueff = U
        b = Cal_distence(POSI[int(LINE[i][0])], POSI[int(LINE[i][1])])
        a = Cal_orientation(POSI[int(LINE[i][0])], POSI[int(LINE[i][1])])
        ren = row * dwhydro * np.linalg.norm(
            (Ueff - np.dot(a, Ueff) * a)) / Dynvis

        Cn = -3.2891e-5 * pow(ren * Sn * Sn,
                              2) + 0.00068 * (ren * Sn * Sn) + 1.4253
        fn = 0.5 * row * dwmesh * (b - dwmesh) * Cn * (
                Ueff - np.dot(a, Ueff) * a) * np.linalg.norm(
            (Ueff - np.dot(a, Ueff) * a))
        # print(a)
        F[int(LINE[i][0])] = F[int(LINE[i][0])] + 0.5 * fn
        F[int(LINE[i][1])] = F[int(LINE[i][1])] + 0.5 * fn
    return F


# >>>>>>>>>>>>>>the following is screen model

def Cal_FS1wake2(POSI, sur, U, Sn, ref):
    # from Aarsnes model(1990) the Sn should be less than 0.35
    # Reynolds number in range from 1400 to 1800
    num_node = len(POSI)
    F = np.zeros((num_node, 3))  # force on nodes
    for i in range(len(sur)):
        # pc = Cal_tricenter(POSI[sur[i][0]], POSI[sur[i][1]], POSI[sur[i][2]])
        # Vwave = wave.Get_Velo(pc, t)
        Ueff = U
        a1 = Cal_orientation(POSI[sur[i][0]], POSI[sur[i][1]])
        a2 = Cal_orientation(POSI[sur[i][0]], POSI[sur[i][2]])
        ba1 = Cal_distence(POSI[sur[i][0]], POSI[sur[i][1]])
        ba2 = Cal_distence(POSI[sur[i][0]], POSI[sur[i][2]])
        surN = np.cross(a1, a2) / np.linalg.norm(np.cross(a1, a2))
        if np.dot(surN, Ueff) < 0:
            surN = -surN
        # the normal vector of the net in positive with current direction
        surL = np.cross(np.cross(Ueff, surN), Ueff) / \
               np.linalg.norm(np.cross(np.cross(Ueff, surN), Ueff) + 0.000000001)
        surA = 0.5 * np.linalg.norm(np.cross(a1 * ba1, a2 * ba2))
        cosalpha = abs(np.dot(surN, Ueff) / np.linalg.norm(Ueff))
        sinalpha = np.linalg.norm(np.cross(surN, Ueff)) / np.linalg.norm(Ueff)
        Cd = 0.04 + (-0.04 + Sn - 1.24 * pow(Sn, 2) +
                     13.7 * pow(Sn, 3)) * cosalpha
        Cl = (0.57 * Sn - 3.54 * pow(Sn, 2) +
              10.1 * pow(Sn, 3)) * 2 * sinalpha * cosalpha
        if i in ref:
            redu = reductionfactorblvin(np.arccos(cosalpha), coe35)
            Ueff = redu * U
        fd = 0.5 * row * surA * Cd * np.linalg.norm(Ueff) * Ueff
        fl = 0.5 * row * surA * Cl * pow(np.linalg.norm(Ueff), 2) * surL
        F[sur[i][0]] = F[sur[i][0]] + (fd + fl) / 6
        F[sur[i][1]] = F[sur[i][1]] + (fd + fl) / 6
        F[sur[i][2]] = F[sur[i][2]] + (fd + fl) / 6
    return F


def Cal_FS1nowake(POSI, sur, U, Sn, ref):
    # from Aarsnes model(1990) the Sn should be less than 0.35
    # Reynolds number in range from 1400 to 1800
    num_node = len(POSI)
    F = np.zeros((num_node, 3))  # force on nodes
    Ueff = U
    for i in range(len(sur)):
        a1 = Cal_orientation(POSI[sur[i][0]], POSI[sur[i][1]])
        a2 = Cal_orientation(POSI[sur[i][0]], POSI[sur[i][2]])
        ba1 = Cal_distence(POSI[sur[i][0]], POSI[sur[i][1]])
        ba2 = Cal_distence(POSI[sur[i][0]], POSI[sur[i][2]])
        surN = np.cross(a1, a2) / np.linalg.norm(np.cross(a1, a2))
        if np.dot(surN, Ueff) < 0:
            surN = -surN
        # the normal vector of the net plane in positive with current direction
        surL = np.cross(np.cross(Ueff, surN), Ueff) / \
               np.linalg.norm(np.cross(np.cross(Ueff, surN), Ueff) + 0.000000001)
        surA = 0.5 * np.linalg.norm(np.cross(a1 * ba1, a2 * ba2))
        cosalpha = abs(np.dot(surN, Ueff) / np.linalg.norm(Ueff))
        sinalpha = np.linalg.norm(np.cross(surN, Ueff)) / np.linalg.norm(Ueff)
        Cd = 0.04 + (-0.04 + Sn - 1.24 * pow(Sn, 2) +
                     13.7 * pow(Sn, 3)) * cosalpha
        Cl = (0.57 * Sn - 3.54 * pow(Sn, 2) +
              10.1 * pow(Sn, 3)) * 2 * sinalpha * cosalpha

        fd = 0.5 * row * surA * Cd * np.linalg.norm(Ueff) * Ueff
        fl = 0.5 * row * surA * Cl * pow(np.linalg.norm(Ueff), 2) * surL
        F[sur[i][0]] = F[sur[i][0]] + (fd + fl) / 6
        F[sur[i][1]] = F[sur[i][1]] + (fd + fl) / 6
        F[sur[i][2]] = F[sur[i][2]] + (fd + fl) / 6
    return F


def Cal_FS1wake1(POSI, sur, U, Sn, ref):
    # from Aarsnes model(1990) the Sn should be less than 0.35
    # Reynolds number in range from 1400 to 1800
    num_node = len(POSI)
    F = np.zeros((num_node, 3))  # force on nodes
    for i in range(len(sur)):
        # pc = Cal_tricenter(POSI[sur[i][0]], POSI[sur[i][1]], POSI[sur[i][2]])
        # Vwave = wave.Get_Velo(pc, t)
        Ueff = U
        a1 = Cal_orientation(POSI[sur[i][0]], POSI[sur[i][1]])
        a2 = Cal_orientation(POSI[sur[i][0]], POSI[sur[i][2]])
        ba1 = Cal_distence(POSI[sur[i][0]], POSI[sur[i][1]])
        ba2 = Cal_distence(POSI[sur[i][0]], POSI[sur[i][2]])
        surN = np.cross(a1, a2) / np.linalg.norm(np.cross(a1, a2))
        if np.dot(surN, Ueff) < 0:
            surN = -surN
        # the normal vector of the net plane in positive with current direction
        surL = np.cross(np.cross(Ueff, surN), Ueff) / \
               np.linalg.norm(np.cross(np.cross(Ueff, surN), Ueff) + 0.000000001)
        surA = 0.5 * np.linalg.norm(np.cross(a1 * ba1, a2 * ba2))
        cosalpha = abs(np.dot(surN, Ueff) / np.linalg.norm(Ueff))
        sinalpha = np.linalg.norm(np.cross(surN, Ueff)) / np.linalg.norm(Ueff)
        Cd = 0.04 + (-0.04 + Sn - 1.24 * pow(Sn, 2) +
                     13.7 * pow(Sn, 3)) * cosalpha
        Cl = (0.57 * Sn - 3.54 * pow(Sn, 2) +
              10.1 * pow(Sn, 3)) * 2 * sinalpha * cosalpha

        if i in ref:
            Ueff = U * (1 - 0.46 * Cd)
        fd = 0.5 * row * surA * Cd * np.linalg.norm(Ueff) * Ueff
        fl = 0.5 * row * surA * Cl * pow(np.linalg.norm(Ueff), 2) * surL
        F[sur[i][0]] = F[sur[i][0]] + (fd + fl) / 6
        F[sur[i][1]] = F[sur[i][1]] + (fd + fl) / 6
        F[sur[i][2]] = F[sur[i][2]] + (fd + fl) / 6
    return F


def Cal_FS2wake2(POSI, sur, U, Sn, ref):
    # from Loland model(1991) the Sn should be 0,13-0.35
    # Reynolds number in range from 1400 to 1800
    num_node = len(POSI)
    F = np.zeros((num_node, 3))  # force on nodes
    for i in range(len(sur)):
        Ueff = (U)
        a1 = Cal_orientation(POSI[sur[i][0]], POSI[sur[i][1]])
        a2 = Cal_orientation(POSI[sur[i][0]], POSI[sur[i][2]])
        ba1 = Cal_distence(POSI[sur[i][0]], POSI[sur[i][1]])
        ba2 = Cal_distence(POSI[sur[i][0]], POSI[sur[i][2]])
        surN = np.cross(a1, a2) / np.linalg.norm(np.cross(a1, a2))
        if np.dot(surN, Ueff) < 0:
            surN = -surN
        surL = np.cross(np.cross(Ueff, surN), Ueff) / \
               np.linalg.norm(np.cross(np.cross(Ueff, surN), Ueff) + 0.000000001)
        surA = 0.5 * np.linalg.norm(np.cross(a1 * ba1, a2 * ba2))
        cosalpha = abs(np.dot(surN, Ueff) / np.linalg.norm(Ueff))
        sinalpha = np.linalg.norm(np.cross(surN, Ueff)) / np.linalg.norm(Ueff)
        Cd = 0.04 + (-0.04 + 0.33 * Sn + 6.54 * pow(Sn, 2) -
                     4.88 * pow(Sn, 3)) * cosalpha
        Cl = (-0.05 * Sn + 2.3 * pow(Sn, 2) -
              1.76 * pow(Sn, 3)) * 2 * sinalpha * cosalpha
        if i in ref:
            redu = reductionfactorblvin(np.arccos(cosalpha), coe35)
            Ueff = redu * U
        fd = 0.5 * row * surA * Cd * np.linalg.norm(Ueff) * Ueff
        fl = 0.5 * row * surA * Cl * pow(np.linalg.norm(Ueff), 2) * surL
        F[sur[i][0]] = F[sur[i][0]] + (fd + fl) / 6
        F[sur[i][1]] = F[sur[i][1]] + (fd + fl) / 6
        F[sur[i][2]] = F[sur[i][2]] + (fd + fl) / 6
    return F


def Cal_FS2nowake(POSI, sur, U, Sn, ref):
    # from Loland model(1991) the Sn should be 0,13-0.35
    # Reynolds number in range from 1400 to 1800
    Ueff = U
    num_node = len(POSI)
    F = np.zeros((num_node, 3))  # force on nodes
    for i in range(len(sur)):
        a1 = Cal_orientation(POSI[sur[i][0]], POSI[sur[i][1]])
        a2 = Cal_orientation(POSI[sur[i][0]], POSI[sur[i][2]])
        ba1 = Cal_distence(POSI[sur[i][0]], POSI[sur[i][1]])
        ba2 = Cal_distence(POSI[sur[i][0]], POSI[sur[i][2]])
        surN = np.cross(a1, a2) / np.linalg.norm(np.cross(a1, a2))
        if np.dot(surN, Ueff) < 0:
            surN = -surN
        surL = np.cross(np.cross(Ueff, surN), Ueff) / \
               np.linalg.norm(np.cross(np.cross(Ueff, surN), Ueff) + 0.000000001)
        surA = 0.5 * np.linalg.norm(np.cross(a1 * ba1, a2 * ba2))
        cosalpha = abs(np.dot(surN, Ueff) / np.linalg.norm(Ueff))
        sinalpha = np.linalg.norm(np.cross(surN, Ueff)) / np.linalg.norm(Ueff)
        Cd = 0.04 + (-0.04 + 0.33 * Sn + 6.54 * pow(Sn, 2) -
                     4.88 * pow(Sn, 3)) * cosalpha
        Cl = (-0.05 * Sn + 2.3 * pow(Sn, 2) -
              1.76 * pow(Sn, 3)) * 2 * sinalpha * cosalpha
        fd = 0.5 * row * surA * Cd * np.linalg.norm(Ueff) * Ueff
        fl = 0.5 * row * surA * Cl * pow(np.linalg.norm(Ueff), 2) * surL
        F[sur[i][0]] = F[sur[i][0]] + (fd + fl) / 6
        F[sur[i][1]] = F[sur[i][1]] + (fd + fl) / 6
        F[sur[i][2]] = F[sur[i][2]] + (fd + fl) / 6
    return F


def Cal_FS3wake1(POSI, sur, U, Sn, ref):
    # from Loland model(1991) the Sn should be 0,13-0.35
    # Reynolds number in range from 1400 to 1800
    num_node = len(POSI)
    F = np.zeros((num_node, 3))  # force on nodes
    for i in range(len(sur)):
        Ueff = (U)
        a1 = Cal_orientation(POSI[sur[i][0]], POSI[sur[i][1]])
        a2 = Cal_orientation(POSI[sur[i][0]], POSI[sur[i][2]])
        ba1 = Cal_distence(POSI[sur[i][0]], POSI[sur[i][1]])
        ba2 = Cal_distence(POSI[sur[i][0]], POSI[sur[i][2]])
        surN = np.cross(a1, a2) / np.linalg.norm(np.cross(a1, a2))
        if np.dot(surN, Ueff) < 0:
            surN = -surN
        surL = np.cross(np.cross(Ueff, surN), Ueff) / \
               np.linalg.norm(np.cross(np.cross(Ueff, surN), Ueff) + 0.000000001)
        surA = 0.5 * np.linalg.norm(np.cross(a1 * ba1, a2 * ba2))
        cosalpha = abs(np.dot(surN, Ueff) / np.linalg.norm(Ueff))
        sinalpha = np.linalg.norm(np.cross(surN, Ueff)) / np.linalg.norm(Ueff)
        Cd = 0.04 + (-0.04 + 0.33 * Sn + 6.54 * pow(Sn, 2) -
                     4.88 * pow(Sn, 3)) * cosalpha
        Cl = (-0.05 * Sn + 2.3 * pow(Sn, 2) -
              1.76 * pow(Sn, 3)) * 2 * sinalpha * cosalpha
        if i in ref:
            Ueff = U * (1 - 0.46 * Cd)
        fd = 0.5 * row * surA * Cd * np.linalg.norm(Ueff) * Ueff
        fl = 0.5 * row * surA * Cl * pow(np.linalg.norm(Ueff), 2) * surL
        F[sur[i][0]] = F[sur[i][0]] + (fd + fl) / 6
        F[sur[i][1]] = F[sur[i][1]] + (fd + fl) / 6
        F[sur[i][2]] = F[sur[i][2]] + (fd + fl) / 6
    return F


# def Cal_Fh9(POSI, sur, U, Sn, ref):
#     # from Jiemin Zhan  2003
#     num_node = len(POSI)
#     F = np.zeros((num_node, 3))  # force on nodes
#     for i in range(len(sur)):
#         if i in ref:
#             Ueff = 0.8 * U
#         else:
#             Ueff = U
#         a1 = Cal_orientation(POSI[sur[i][0]], POSI[sur[i][1]])
#         a2 = Cal_orientation(POSI[sur[i][0]], POSI[sur[i][2]])
#         ba1 = Cal_distence(POSI[sur[i][0]], POSI[sur[i][1]])
#         ba2 = Cal_distence(POSI[sur[i][0]], POSI[sur[i][2]])
#         surN = np.cross(a1, a2) / np.linalg.norm(np.cross(a1, a2))
#         if np.dot(surN, Ueff) < 0:
#             surN = -surN
#         surA = 0.5 * np.linalg.norm(np.cross(a1 * ba1, a2 * ba2))
#         cosalpha = abs(np.dot(surN, Ueff) / np.linalg.norm(Ueff))
#         sinalpha = np.linalg.norm(np.cross(surN, Ueff)) / np.linalg.norm(Ueff)
#         Un = abs(np.dot(surN, Ueff) + 0.0000001)  # Un can no be zero
#         Ut = np.linalg.norm(
#             Ueff - np.dot(surN, Ueff) * 0.999999999)  # Ut can no be zero
#         cf = 1 - 0.211 / Ut + 0.947 * Sn
#         cd = 1 + 0.137 / Un + 1.002 * Sn + 2.23 * pow(Sn, 2)
#         Ltotal = surA * Sn / dwhydro
#         R0 = cd * 0.5 * row * np.linalg.norm(Ueff) * Ueff * Ltotal * dwhydro
#         fn = R0 * 0.5 * (1 + pow(cosalpha, 3) + cf * pow(sinalpha, 3) / cd)
#         F[sur[i][0]] = F[sur[i][0]] + (fn) / 6
#         F[sur[i][1]] = F[sur[i][1]] + (fn) / 6
#         F[sur[i][2]] = F[sur[i][2]] + (fn) / 6
#     return F


def Cal_FS3wake1(POSI, sur, U, Sn, ref):
    # from Trygve Kristiansen 2002
    num_node = len(POSI)
    F = np.zeros((num_node, 3))  # force on nodes
    for i in range(len(sur)):
        Ueff = (U)
        a1 = Cal_orientation(POSI[sur[i][0]], POSI[sur[i][1]])
        a2 = Cal_orientation(POSI[sur[i][0]], POSI[sur[i][2]])
        ba1 = Cal_distence(POSI[sur[i][0]], POSI[sur[i][1]])
        ba2 = Cal_distence(POSI[sur[i][0]], POSI[sur[i][2]])
        surN = np.cross(a1, a2) / np.linalg.norm(np.cross(a1, a2))
        if np.dot(surN, Ueff) < 0:
            surN = -surN
        surL = np.cross(np.cross(Ueff, surN), Ueff) / \
               np.linalg.norm(np.cross(np.cross(Ueff, surN), Ueff) + 0.000000001)
        surA = 0.5 * np.linalg.norm(np.cross(a1 * ba1, a2 * ba2))
        alpha = np.arccos(abs(np.dot(surN, Ueff) / np.linalg.norm(Ueff)))
        Re = row * dwhydro * np.linalg.norm(Ueff) / Dynvis / (1 - Sn)
        cdcyl = -78.46675 + 254.73873 * np.log10(Re) - 327.8864 * pow(
            np.log10(Re), 2) + 223.64577 * pow(np.log10(
            Re), 3) - 87.92234 * pow(np.log10(Re), 4) + 20.00769 * pow(
            np.log10(Re), 5) - 2.44894 * pow(
            np.log10(Re), 6) + 0.12479 * pow(np.log10(Re), 7)
        Cd0 = cdcyl * (Sn * (2 - Sn)) / (2.0 * pow((1 - Sn), 2))
        Cl0 = pi * cdcyl * Sn / pow(1 - Sn,
                                    2) / (8 + cdcyl * Sn / pow(1 - Sn, 2))

        Cd = Cd0 * (0.75 * np.cos(alpha) + 0.25 * np.cos(3 * alpha))
        Cl = Cl0 * (0.9 * np.sin(2 * alpha) + 0.1 * np.sin(4 * alpha))
        if i in ref:
            Ueff = (1 - 0.46 * Cd) * U
        fd = 0.5 * row * surA * Cd * np.linalg.norm(Ueff) * Ueff
        fl = 0.5 * row * surA * Cl * pow(np.linalg.norm(Ueff), 2) * surL
        F[sur[i][0]] = F[sur[i][0]] + (fd + fl) / 6
        F[sur[i][1]] = F[sur[i][1]] + (fd + fl) / 6
        F[sur[i][2]] = F[sur[i][2]] + (fd + fl) / 6
    return F


def Cal_FS3wake2(POSI, sur, U, Sn, ref):
    # from Trygve Kristiansen 2002
    num_node = len(POSI)
    F = np.zeros((num_node, 3))  # force on nodes
    for i in range(len(sur)):
        Ueff = (U)
        a1 = Cal_orientation(POSI[sur[i][0]], POSI[sur[i][1]])
        a2 = Cal_orientation(POSI[sur[i][0]], POSI[sur[i][2]])
        ba1 = Cal_distence(POSI[sur[i][0]], POSI[sur[i][1]])
        ba2 = Cal_distence(POSI[sur[i][0]], POSI[sur[i][2]])
        surN = np.cross(a1, a2) / np.linalg.norm(np.cross(a1, a2))
        if np.dot(surN, Ueff) < 0:
            surN = -surN
        surL = np.cross(np.cross(Ueff, surN), Ueff) / \
               np.linalg.norm(np.cross(np.cross(Ueff, surN), Ueff) + 0.000000001)
        surA = 0.5 * np.linalg.norm(np.cross(a1 * ba1, a2 * ba2))
        alpha = np.arccos(abs(np.dot(surN, Ueff) / np.linalg.norm(Ueff)))
        Re = row * dwhydro * np.linalg.norm(Ueff) / Dynvis / (1 - Sn)
        cdcyl = -78.46675 + 254.73873 * np.log10(Re) - 327.8864 * pow(
            np.log10(Re), 2) + 223.64577 * pow(np.log10(
            Re), 3) - 87.92234 * pow(np.log10(Re), 4) + 20.00769 * pow(
            np.log10(Re), 5) - 2.44894 * pow(
            np.log10(Re), 6) + 0.12479 * pow(np.log10(Re), 7)
        Cd0 = cdcyl * (Sn * (2 - Sn)) / (2.0 * pow((1 - Sn), 2))
        Cl0 = pi * cdcyl * Sn / pow(1 - Sn,
                                    2) / (8 + cdcyl * Sn / pow(1 - Sn, 2))

        Cd = Cd0 * (0.75 * np.cos(alpha) + 0.25 * np.cos(3 * alpha))
        Cl = Cl0 * (0.9 * np.sin(2 * alpha) + 0.1 * np.sin(4 * alpha))
        if i in ref:
            redu = reductionfactorblvin(np.cos(alpha), coe20)
            Ueff = redu * U
        fd = 0.5 * row * surA * Cd * np.linalg.norm(Ueff) * Ueff
        fl = 0.5 * row * surA * Cl * pow(np.linalg.norm(Ueff), 2) * surL
        F[sur[i][0]] = F[sur[i][0]] + (fd + fl) / 6
        F[sur[i][1]] = F[sur[i][1]] + (fd + fl) / 6
        F[sur[i][2]] = F[sur[i][2]] + (fd + fl) / 6
    return F


def Cal_FS4(POSI, sur, U, Sn, ref):
    #   based on a Fridman 1975
    num_node = len(POSI)
    F = np.zeros((num_node, 3))  # force on nodes
    for i in range(len(sur)):
        if i in ref:
            Ueff = 0.8 * U
        else:
            Ueff = U
        Re = np.linalg.norm(Ueff) * dwhydro * row / Dynvis
        Rey = Re / (2 * Sn)
        Ct = 0.1 * pow(Re, 0.14) * Sn
        Cn = 3 * pow(Rey, -0.07) * Sn
        # print(Cn)
        a1 = Cal_orientation(POSI[sur[i][0]], POSI[sur[i][1]])
        a2 = Cal_orientation(POSI[sur[i][0]], POSI[sur[i][2]])
        ba1 = Cal_distence(POSI[sur[i][0]], POSI[sur[i][1]])
        ba2 = Cal_distence(POSI[sur[i][0]], POSI[sur[i][2]])
        surN = np.cross(a1, a2) / np.linalg.norm(np.cross(a1, a2))
        surA = 0.5 * np.linalg.norm(np.cross(a1 * ba1, a2 * ba2))
        fn = 0.5 * row * surA * Cn * np.dot(surN, Ueff) * \
             surN * np.linalg.norm(np.dot(surN, Ueff) * surN)
        ft = 0.5 * row * surA * Ct * (Ueff - np.dot(surN, Ueff) * surN) * \
             np.linalg.norm(Ueff - np.dot(surN, Ueff) * surN)
        F[sur[i][0]] = F[sur[i][0]] + (fn + ft) / 6
        F[sur[i][1]] = F[sur[i][1]] + (fn + ft) / 6
        F[sur[i][2]] = F[sur[i][2]] + (fn + ft) / 6
    return F


def Cal_FS5(POSI, sur, U, Sn, ref):
    # from chun woo lee (2005)
    num_node = len(POSI)
    F = np.zeros((num_node, 3))  # force on nodes
    for i in range(len(sur)):
        Ueff = (U)
        a1 = Cal_orientation(POSI[sur[i][0]], POSI[sur[i][1]])
        a2 = Cal_orientation(POSI[sur[i][0]], POSI[sur[i][2]])
        ba1 = Cal_distence(POSI[sur[i][0]], POSI[sur[i][1]])
        ba2 = Cal_distence(POSI[sur[i][0]], POSI[sur[i][2]])
        surN = np.cross(a1, a2) / np.linalg.norm(np.cross(a1, a2))
        if np.dot(surN, Ueff) < 0:
            surN = -surN
        surL = np.cross(np.cross(Ueff, surN), Ueff) / \
               np.linalg.norm(np.cross(np.cross(Ueff, surN), Ueff) + 0.000000001)
        surA = 0.5 * np.linalg.norm(np.cross(a1 * ba1, a2 * ba2))
        cosalpha = abs(np.dot(surN, Ueff) / np.linalg.norm(Ueff))
        alf = np.arccos(abs(np.dot(surN, Ueff) / np.linalg.norm(Ueff)))
        Cd = 0.556 * pow(alf, 7) - 1.435 * pow(alf, 6) - 2.403 * pow(
            alf, 5) + 11.75 * pow(alf, 4) - 13.48 * pow(alf, 3) + 5.079 * pow(
            alf, 2) - 0.9431 * pow(alf, 1) + 1.155
        Cl = -10.22 * pow(alf, 9) + 69.22 * pow(alf, 8) - 187.9 * pow(
            alf, 7) + 257.3 * pow(alf, 6) - 181.6 * pow(alf, 5) + 59.14 * pow(
            alf, 4) - 7.97 * pow(alf, 3) + 2.103 * pow(
            alf, 2) + 0.2325 * pow(alf, 1) + 0.01294
        if i in ref:
            redu = reductionfactorblvin(cosalpha, coe25)
            Ueff = redu * U
        fd = 0.5 * row * surA * Cd * Sn * np.linalg.norm(Ueff) * Ueff
        fl = 0.5 * row * surA * Cl * Sn * pow(np.linalg.norm(Ueff), 2) * surL
        F[sur[i][0]] = F[sur[i][0]] + (fd + fl) / 6
        F[sur[i][1]] = F[sur[i][1]] + (fd + fl) / 6
        F[sur[i][2]] = F[sur[i][2]] + (fd + fl) / 6
    return F


def Cal_FS6(POSI, sur, U, Sn, ref):
    # from Balash 2009
    num_node = len(POSI)
    F = np.zeros((num_node, 3))  # force on nodes
    for i in range(len(sur)):
        if i in ref:
            Ueff = 0.8 * U
        else:
            Ueff = U
        a1 = Cal_orientation(POSI[sur[i][0]], POSI[sur[i][1]])
        a2 = Cal_orientation(POSI[sur[i][0]], POSI[sur[i][2]])
        ba1 = Cal_distence(POSI[sur[i][0]], POSI[sur[i][1]])
        ba2 = Cal_distence(POSI[sur[i][0]], POSI[sur[i][2]])
        surN = np.cross(a1, a2) / np.linalg.norm(np.cross(a1, a2))
        if np.dot(surN, Ueff) < 0:
            surN = -surN
        surA = 0.5 * np.linalg.norm(np.cross(a1 * ba1, a2 * ba2))
        cosalpha = abs(np.dot(surN, Ueff) / np.linalg.norm(Ueff))
        # sinalpha = np.linalg.norm(np.cross(surN, Ueff))/np.linalg.norm(Ueff)
        Re = row * dwhydro * Ueff / Dynvis / (1 - Sn) + 0.000001
        cdcyl = 1 + 10.0 / (pow(Re, 2.0 / 3.0))
        Cd = cdcyl * (0.12 - 0.74 * Sn + 8.03 * pow(Sn, 2)) * pow(cosalpha, 3)
        fd = 0.5 * row * surA * Cd * np.linalg.norm(Ueff) * Ueff
        F[sur[i][0]] = F[sur[i][0]] + fd / 6
        F[sur[i][1]] = F[sur[i][1]] + fd / 6
        F[sur[i][2]] = F[sur[i][2]] + fd / 6
    return F
