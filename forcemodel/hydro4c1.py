# writer: hui.cheng@uis.no
import numpy as np
from numpy import pi

# it must define in the comm file
row = 1025  # kg/m3   sea water density
Kinvis = 1.004e-6  # when the water tempreture is 20 degree.
Dynvis = 1.002e-3  # when the water tempreture is 20 degree.


class Net2NetWake:
    def __init__(self, posi, hydroelement, U, Sn):
        self.posi = []  # a list of all the nodes for net
        self.hydroelement = []  # a list of all the elements for net
        self.U = []  # incoming velocity for cage
        self.cagecenter = np.zeros((3, 1))  # set the cage center is [0,0,0]
        self.elem_shie = []
        self.Sn = Sn
        self.coe25 = np.array(
            [-2.892133401021243500e-01, 6.267135574694910893e-01, -7.157409449812776603e-02, -8.320909217614042008e-01,
             7.398392740943907642e-01, -2.683467821216800053e-01, 1.949719351189289560e-02, 8.249793665980104107e-01])
        self.coe20 = np.array(
            [-1.474349975132451362e+00, 6.490272947305592233e+00, -1.146253302377779626e+01, 1.016432973554554842e+01,
             -4.699724398373956724e+00, 1.002973285638476986e+00, -8.328579182908107947e-02,
             8.608477553083272449e-01, ])
        self.coe35 = np.array([-4.25657, 18.6974, -32.7564, 28.8642, -13.4061, 3.0472, -0.304585, 0.885381, ])

    def getpaneslinwake(self):
        elem_shie = []
        for i in range(len(self.hydroelement)):
            elmentcenter = Cal_tricenter(self.posi[self.hydroelement[i][0]],
                                         self.posi[self.hydroelement[i][1]],
                                         self.posi[self.hydroelement[i][2]])
            vectortocagecenter = (elmentcenter - self.cagecenter)
            if np.dot(vectortocagecenter, self.U) < 0:
                elem_shie.append(i)
        return self.elem_shie

    def getlinesinwake(self):
        elem_shie = []
        for i in range(len(self.hydroelement)):
            elmentcenter = Cal_linecenter(
                self.posi[int(self.hydroelement[i][0])],
                self.posi[int(self.hydroelement[i][1])])
            vectortocagecenter = (elmentcenter - self.cagecenter)
            if np.dot(vectortocagecenter, self.U) < 0:
                elem_shie.append(i)
        return self.elem_shie

    def reductionfactorblvin(self, alf):  # alf is the inflow angle
        refa = 0
        alf = np.abs(alf)
        if self.Sn < 0.22:
            coe = self.coe20
        elif self.Sn < 0.32:
            coe = self.coe25
        else:
            coe = self.coe30
        for i in range(len(coe) - 1):
            refa += coe[i] * pow(abs(alf), 7 - i)
        return refa + 0.825


class HydroMorison:
    """
    For Morison hydrodyanmic models, the code needs the nodes' potions \n
    and the connetions.  \n
    Thus, the input variable is the matrix of nodes and the connetions. \n
    In addition, the solidity and constant flow reduction are also needed.
    """

    def __init__(self, posimatrix, hydroelem, solidity, dwh=0.0, dw0=0.0):
        self.posi = posimatrix  # the position matrix [[x1,y1,z1][x2,y2,z2]]
        self.hydroelem = hydroelem  # the connections of the twines[[p1,p2][p2,p3]]
        self.dwh = dwh  # used for the force calculation (reference area)
        # can be a consistent number or a list
        self.dw0 = dw0  # used for the hydrodynamic coefficients
        # can be a consistent number or a list
        self.Sn = solidity

    def M1(self, U):
        # ref is a list of which elements in the wake region
        # ref. J.S. Bessonneau and D. Marichal. 1998 # cd=1.2,ct=0.1.
        num_node = len(self.posi)
        num_line = len(self.line)
        if len(self.dwh) == 1:
            dwh = self.dwh * np.ones((num_line, 1))
        # if len(self.dw0) == 1:
        #     dw0 = self.dw0 * np.ones((num_line, 1))
        Ct = 0.1
        Cn = 1.2
        wake = Net2NetWake(self.posi, self.hydroelem, U, self.Sn)
        ref = wake.getlinesinwake()
        a = []  # oriention for the cable
        b = []  # cable length
        F = np.zeros((num_node, 3))  # force on nodes
        for i in range(num_line):
            Ueff = U
            b = Cal_distence(self.posi[self.line[i][0]], self.posi[self.line[i][1]])
            a = Cal_orientation(self.posi[self.line[i][0]], self.posi[self.line[i][1]])
            if i in ref:
                Ueff = 0.8 * U
            ft = 0.5 * row * dwh[i] * (b - dwh[i]) * Ct * pow(np.dot(a, Ueff), 2) * a
            fn = 0.5 * row * dwh[i] * (b - dwh[i]) * Cn * (
                    Ueff - np.dot(a, Ueff) * a) * np.linalg.norm(
                (Ueff - np.dot(a, Ueff) * a))
            F[int(self.line[i][0])] = F[int(self.line[i][0])] + 0.5 * (fn + ft)
            F[int(self.line[i][1])] = F[int(self.line[i][1])] + 0.5 * (fn + ft)
        return F


# for functions used in the current file
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
    return np.transpose(POSI)


def Get_velo(tabreu):  # to get the velocity
    CxT2 = tabreu.EXTR_TABLE()
    VX1 = CxT2.values()['DX']
    VX2 = CxT2.values()['DY']
    VX3 = CxT2.values()['DZ']
    VITE = np.array([VX1, VX2, VX3])
    return np.transpose(VITE)
