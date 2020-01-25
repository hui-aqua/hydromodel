import numpy as np

with open('../benchMarkTests/moe2016/cageDict', 'r') as f:
    content = f.read()
    reread = eval(content)
print(reread['Environment']['fluidDensity'])
with open('meshinfomation.txt', 'r') as f:
    content = f.read()
    mesh = eval(content)
row = 1025  # kg/m3   sea water density


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


def Cal_element(eachpanel, realtimeposi, origvelo):
    # because the mesh construction, the first two node cannot have same index

    a1 = Cal_orientation(realtimeposi[eachpanel[0]], realtimeposi[eachpanel[1]])
    print('a1=', a1)
    a2 = Cal_orientation(realtimeposi[eachpanel[0]], realtimeposi[eachpanel[2]])
    print('a2=', a2)
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
        print("the index of the elements in the wake is saved")
        return self.ref

    def S1(self, realtimeposi, U):
        print('the number of node is ' + str(realtimeposi))
        # from Aarsnes model(1990) the Sn should be less than 0.35
        # Reynolds number in range from 1400 to 1800
        num_node = len(self.posi)  # the number of the node
        print('the number of node is ' + str(num_node))
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
                print('there are 3 nodes on this hydro element')
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
                    print('there are 4 nodes on this hydro element')
                    nodes = [int(k) for k in panel]  # get the list of nodes [p1,p2,p3,p4]
                    print('Now nodes ' + str(nodes))
                    nodes.pop(i)  # delete the i node to make the square to a triangle
                    panelInSquare = nodes
                    print('Now the pane in square is ' + str(panelInSquare))
                    alpha, surN, surL, surA = Cal_element(panelInSquare, realtimeposi,
                                                          U)  # calculate the inflow angel, normal vector, lift force factor, area of the hydrodyanmic element
                    print('Now the pane proposity is ' + str(alpha) + '\n' + str(surN) + '\n' + str(surL) + '\n' + str(
                        surA))
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


posi = np.loadtxt("posi0.0.txt")
sur = mesh["netSurfaces"]
u = np.array([0.069, 0, 0])
hymo = HydroScreen(posi, sur, 0.12, u, 0.0012, 0.0012)
elementinwake = hymo.Save_ref()
np.savetxt('elementinwake.txt', elementinwake)

Fnh = hymo.S1(posi, u)
try:
    print(x)
except:
    print("An exception occurred")
