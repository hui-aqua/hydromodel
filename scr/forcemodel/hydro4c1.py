"""
/--------------------------------\
|    University of Stavanger     |
|           Hui Cheng            |
\--------------------------------/
Any questions about this code, please email: hui.cheng@uis.no
A module can be used to calculate the hydrodynamic forces on nets in Code_Aster.
To use this module, one should be import this into the input file for calculations.
"""
import time
import pickle
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

    def __init__(self, modelIndex, posimatrix, hydroelem, solidity, Udirection, dwh=0.0, dw0=0.0):
        self.modelIndex = str(modelIndex)
        self.posi = posimatrix  # the position matrix [[x1,y1,z1][x2,y2,z2]]
        self.hydroelem = hydroelem  # the connections of the twines[[p1,p2][p2,p3]]
        self.dwh = dwh  # used for the force calculation (reference area)
        # can be a consistent number or a list
        self.dw0 = dw0  # used for the hydrodynamic coefficients
        # can be a consistent number or a list
        self.Sn = solidity
        wake = Net2NetWake(self.posi, self.hydroelem, Udirection, self.Sn)
        self.ref = wake.geteleminwake()
        self.hydroForces_Element = np.zeros((len(hydroelem), 3))

    def Save_ref(self):
        return self.ref

    def hydroCoefficients(self, U, knot=False):
        dragNorm = 0
        dragTang = 0
        if self.modelIndex not in 'S1,S2,S3,S4,S5,S6':
            print("The selected hydrodynamic model is not included in the present program")
            exit()
        elif self.modelIndex == 'M1':  # Bessonneau 1998
            dragNorm = 1.2
            dragTang = 0.1
        elif self.modelIndex == 'M2':  # Wan 2002
            dragNorm = 1.3
            dragTang = 0.0
        elif self.modelIndex == 'M3':  # Takagi 2004
            Re = row * self.dw0 * np.linalg.norm(U) / Dynvis
            if Re < 200:
                dragNorm = pow(10, 0.7) * pow(Re, -0.3)
            else:
                dragNorm = 1.2
            dragTang = 0.1
        elif self.modelIndex == 'M4':  # choo 1971
            Re = row * self.dw0 * np.linalg.norm(U) / Dynvis
            dragTang = np.pi * Dynvis * (0.55 * np.sqrt(Re) + 0.084 * pow(Re, 2.0 / 3.0))
            s = -0.07721565 + np.log(8.0 / Re)
            if 0 < Re < 1:
                dragNorm = 8 * np.pi * (1 - 0.87 * pow(s, -2)) / (s * Re)
            elif Re < 30:
                dragNorm = 1.45 + 8.55 * pow(Re, -0.9)
            elif Re < 2.33e5:
                dragNorm = 1.1 + 4 * pow(Re, -0.5)
            elif Re < 4.92e5:
                dragNorm = (-3.41e-6) * (Re - 5.78e5)
            elif Re < 1e7:
                dragNorm = 0.401 * (1 - np.exp(-Re / 5.99 * 1e5))
            else:
                print("Reynold number=" + str(Re) + ", and it exceeds the range.")
                exit()
        return dragNorm, dragTang

    def elementForce(self, realtimeposi, U):
        """
        :param realtimeposi: a list of positions of all nodes
        :param U: [ux,uy,uz], Unit [m/s]
        :return: update the self.hydroForces_Element
        """
        num_line = len(self.hydroelem)
        hydroForce_on_element = []  # force on line element, initial as zeros
        for i in range(num_line):
            b = Cal_distence(realtimeposi[int(self.hydroelem[i][0])], realtimeposi[int(self.hydroelem[i][1])])
            a = Cal_orientation(realtimeposi[int(self.hydroelem[i][0])], realtimeposi[int(self.hydroelem[i][1])])
            if i in self.ref:
                Ueff = 0.8 * np.array(U)
            else:
                Ueff = np.array(U)
            Cn, Ct = self.hydroCoefficients(U, knot=False)
            # Cn, Ct = self.M5(Ueff) if M5 is applied
            ft = 0.5 * row * self.dwh * (b - self.dwh) * Ct * np.dot(a, Ueff) * a * np.linalg.norm(np.dot(a, Ueff))
            fn = 0.5 * row * self.dwh * (b - self.dwh) * Cn * (Ueff - np.dot(a, Ueff) * a) * np.linalg.norm(
                (Ueff - np.dot(a, Ueff) * a))
            hydroForce_on_element.append(ft + fn)
        self.hydroForces_Element = np.array(hydroForce_on_element)

    def distributeForce(self):
        """
        Transfer the forces on line element to their corresponding nodes
        :return: hydroForces_nodes
        """
        force_on_nodes = np.zeros((len(self.posi), 3))  # force on nodes, initial as zeros
        for line in self.hydroelems:
            force_on_nodes[line[0]] += (self.hydroForces_Element[self.hydroelems.index(line)]) / 2
            force_on_nodes[line[1]] += (self.hydroForces_Element[self.hydroelems.index(line)]) / 2
        return force_on_nodes


class HydroScreen:
    """
    For Screen hydrodynamic models, the code needs the panel' potions \n
    and the connections.  \n
    Thus, the input variable is the matrix of nodes and the connetions. \n
    In addition, the solidity and constant flow reduction are also needed.
    """

    def __init__(self, modelIndex, posiMatrix, hydroelems, solidity, Udirection, dwh=0.0, dw0=0.0):
        self.modelIndex = str(modelIndex)
        self.node_position = posiMatrix  # the position matrix [[x1,y1,z1][x2,y2,z2]]
        self.hydro_element = self.convert_hydro_element(hydroelems)  # the connections of the twines[[p1,p2][p2,p3]]
        self.dwh = dwh  # used for the force calculation (reference area)
        self.dw0 = dw0  # used for the hydrodynamic coefficients
        self.Sn = solidity  # solidity of th net
        self.wake = Net2NetWake(self.node_position, self.hydro_element, Udirection, self.Sn)  # create wake object
        self.ref = self.wake.geteleminwake()  # get the elements in the wake
        self.force_on_elements = np.zeros((len(self.hydro_element), 3))

    def Save_ref(self):
        # return the index of the elements in the wake region
        return self.ref

    def Save_hydroelems(self):
        # return the index of the elements in the wake region
        return self.hydro_element

    def convert_hydro_element(self, hydroE):
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

    def hydroCoefficients(self, inflow_angle, current_velocity, knot=False):
        drag_coefficient, lift_coefficient = 0, 0
        if self.modelIndex not in 'S1,S2,S3,S4,S5,S6':
            print("The selected hydrodynamic model is not included in the present program")
            exit()
        elif self.modelIndex == 'S1':  # aarsnes 1990
            drag_coefficient = 0.04 + (-0.04 + self.Sn - 1.24 * pow(self.Sn, 2) + 13.7 * pow(self.Sn, 3)) * np.cos(
                inflow_angle)
            lift_coefficient = (0.57 * self.Sn - 3.54 * pow(self.Sn, 2) + 10.1 * pow(self.Sn, 3)) * np.sin(
                2 * inflow_angle)

        elif self.modelIndex == 'S2':  # Loland 1991
            drag_coefficient = 0.04 + (
                    -0.04 + 0.33 * self.Sn + 6.54 * pow(self.Sn, 2) - 4.88 * pow(self.Sn, 3)) * np.cos(
                inflow_angle)
            lift_coefficient = (-0.05 * self.Sn + 2.3 * pow(self.Sn, 2) - 1.76 * pow(self.Sn, 3)) * np.sin(
                2 * inflow_angle)

        elif self.modelIndex == 'S3':  # Kristiansen 2012
            a1 = 0.9
            a3 = 0.15
            b2 = 0.8
            b4 = 0.2
            reynolds_number = row * self.dw0 * np.linalg.norm(current_velocity) / Dynvis / (1 - self.Sn)  # Re
            cd_cylinder = -78.46675 + 254.73873 * np.log10(reynolds_number) - 327.8864 * pow(np.log10(reynolds_number),
                                                                                             2) + 223.64577 * pow(
                np.log10(reynolds_number),
                3) - 87.92234 * pow(
                np.log10(reynolds_number), 4) + 20.00769 * pow(np.log10(reynolds_number), 5) - 2.44894 * pow(
                np.log10(reynolds_number), 6) + 0.12479 * pow(
                np.log10(reynolds_number), 7)
            cd_zero = cd_cylinder * (self.Sn * (2 - self.Sn)) / (2.0 * pow((1 - self.Sn), 2))
            cl_zero = np.pi * cd_cylinder * self.Sn / pow(1 - self.Sn, 2) / (
                    8 + cd_cylinder * self.Sn / pow(1 - self.Sn, 2))
            drag_coefficient = cd_zero * (a1 * np.cos(inflow_angle) + a3 * np.cos(3 * inflow_angle))
            lift_coefficient = cl_zero * (b2 * np.sin(2 * inflow_angle) + b4 * np.sin(4 * inflow_angle))

        elif self.modelIndex == 'S4':  # Fridman 1973
            reynolds_number = np.linalg.norm(current_velocity) * self.dw0 * row / Dynvis
            reynolds_star = reynolds_number / (2 * self.Sn)
            coe_tangent = 0.1 * pow(reynolds_number, 0.14) * self.Sn
            coe_normal = 3 * pow(reynolds_star, -0.07) * self.Sn
            drag_coefficient = coe_normal * np.cos(inflow_angle) * pow(np.cos(inflow_angle), 2) + coe_tangent * np.sin(
                inflow_angle) * pow(
                np.sin(inflow_angle), 2)
            lift_coefficient = coe_normal * np.sin(inflow_angle) * pow(np.cos(inflow_angle), 2) + coe_tangent * np.cos(
                inflow_angle) * pow(
                np.sin(inflow_angle), 2)
        elif self.modelIndex == 'S5':  # Lee 2005 # polynomial fitting
            drag_coefficient = 0.556 * pow(inflow_angle, 7) - 1.435 * pow(inflow_angle, 6) - 2.403 * pow(
                inflow_angle, 5) + 11.75 * pow(inflow_angle, 4) - 13.48 * pow(inflow_angle, 3) + 5.079 * pow(
                inflow_angle, 2) - 0.9431 * pow(inflow_angle, 1) + 1.155
            lift_coefficient = -10.22 * pow(inflow_angle, 9) + 69.22 * pow(inflow_angle, 8) - 187.9 * pow(
                inflow_angle, 7) + 257.3 * pow(inflow_angle, 6) - 181.6 * pow(inflow_angle, 5) + 59.14 * pow(
                inflow_angle, 4) - 7.97 * pow(inflow_angle, 3) + 2.103 * pow(
                inflow_angle, 2) + 0.2325 * pow(inflow_angle, 1) + 0.01294

        elif self.modelIndex == 'S6':  # Balash 2009
            reynolds_cylinder = row * self.dw0 * np.linalg.norm(current_velocity) / Dynvis / (1 - self.Sn) + 0.000001
            cd_cylinder = 1 + 10.0 / (pow(reynolds_cylinder, 2.0 / 3.0))
            drag_coefficient = cd_cylinder * (0.12 - 0.74 * self.Sn + 8.03 * pow(self.Sn, 2)) * pow(inflow_angle, 3)
            if knot:
                mesh_size = 10 * self.dw0  # assume Sn=0.2
                diameter_knot = 2 * self.dw0  # assume the knot is twice of the diameter of the twine
                reynolds_sphere = row * diameter_knot * np.linalg.norm(current_velocity) / Dynvis / (
                        1 - self.Sn) + 0.000001
                coe_sphere = 24.0 / reynolds_sphere + 6.0 / (1 + np.sqrt(reynolds_sphere)) + 0.4
                drag_coefficient = (cd_cylinder * 8 * pow(diameter_knot,
                                                          2) + coe_sphere * np.pi * mesh_size * self.dw0) / np.pi * mesh_size * self.dw0 * (
                                           0.12 - 0.74 * self.Sn + 8.03 * pow(self.Sn, 2)) * pow(inflow_angle, 3)
            else:
                pass
        return drag_coefficient, lift_coefficient

    def elementForce(self, realTimePositions, U):
        """
        :param realTimePositions: a list of positions of all nodes
        :param U: [ux,uy,uz], Unit [m/s]
        :return:  update the self.hydroForces_Element
        """
        hydroForce_elements = []  # force on net panel, initial as zeros
        for panel in self.hydro_element:  # loop based on the hydrodynamic elements
            p1 = realTimePositions[panel[0]]
            p2 = realTimePositions[panel[1]]
            p3 = realTimePositions[panel[2]]
            alpha, surN, surL, surA = Cal_element(p1, p2, p3, U)
            # calculate the inflow angel, normal vector, lift force factor, area of the hydrodynamic element
            # set([int(k) for k in set(panel)])   # get a set of the node sequence in the element
            if self.hydro_element.index(panel) in self.ref:  # if the element in the wake region
                Ueff = U * self.wake.reductionfactor2(alpha) * 0.8 ** int(
                    (self.hydro_element.index(panel) + 1) / 672)  # the effective velocity = U* reduction factor
            else:
                Ueff = U * 0.8 ** int((self.hydro_element.index(
                    panel) + 1) / 672)  # if not in the wake region, the effective velocity is the undisturbed velocity

            Cd, Cl = self.hydroCoefficients(alpha, Ueff, knot=False)
            fd = 0.5 * row * surA * Cd * np.linalg.norm(Ueff) * Ueff
            fl = 0.5 * row * surA * Cl * pow(np.linalg.norm(Ueff), 2) * surL
            hydroForce_elements.append((fd + fl) / 2.0)
        if np.size(np.array(hydroForce_elements)) == np.size(self.hydro_element):
            self.force_on_elements = np.array(hydroForce_elements)
        else:
            print("\nError! the size of hydrodynamic force on element is not equal to the number of element."
                  "\nPlease cheack you code.")
            print("\nThe size of element is " + str(len(self.hydro_element)))
            print("\nThe size of hydrodynamic force is " + str(len(np.array(hydroForce_elements))))
            exit()

    def screenFsi(self, realTimePositions, Ufluid):
        """
        :param realTimePositions: a list of positions of all nodes
        :param Ufluid: a list of velocity on the centers of all net panels
        :return: update the self.hydroForces_Element and output the forces on all the net panels.
        """
        print("The length of U vector is " + str(len(Ufluid)))
        hydroForce_elements = []  # force on netpanel, initial as zeros
        for panel in self.hydro_element:  # loop based on the hydrodynamic elements
            U = Ufluid[self.hydro_element.index(panel)]
            p1 = realTimePositions[panel[0]]
            p2 = realTimePositions[panel[1]]
            p3 = realTimePositions[panel[2]]
            alpha, surN, surL, surA = Cal_element(p1, p2, p3, U)
            Cd, Cl = self.hydroCoefficients(alpha, U, knot=False)
            fd = 0.5 * row * surA * Cd * np.linalg.norm(np.array(U)) * np.array(U)
            fl = 0.5 * row * surA * Cl * pow(np.linalg.norm(U), 2) * surL
            hydroForce_elements.append((fd + fl) / 2.0)
        if np.size(np.array(hydroForce_elements)) == np.size(self.hydro_element):
            self.force_on_elements = np.array(hydroForce_elements)
            return np.array(hydroForce_elements)
        else:
            print("Error!, the size of hydrodynamic force on element is not equal to the number of element."
                  "Please cheack you code.")
            exit()

    def distribute_force(self):
        """
        Transfer the forces on net panels to their corresponding nodes
        :return: hydroForces_nodes
        """
        forces_on_nodes = np.zeros((len(self.node_position), 3))  # force on nodes, initial as zeros
        for panel in self.hydro_element:
            forces_on_nodes[panel[0]] += (self.force_on_elements[self.hydro_element.index(panel)]) / 3
            forces_on_nodes[panel[1]] += (self.force_on_elements[self.hydro_element.index(panel)]) / 3
            forces_on_nodes[panel[2]] += (self.force_on_elements[self.hydro_element.index(panel)]) / 3
        # print("The force on nodes are" + str(hydroForces_nodes))
        return forces_on_nodes


## - five functions used in the current file

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
    # print('In hy, the posi is'+str(np.transpose(POSI)))
    return np.transpose(POSI)


def Get_velo(tabreu):  # to get the velocity
    CxT2 = tabreu.EXTR_TABLE()
    VX1 = CxT2.values()['DX']
    VX2 = CxT2.values()['DY']
    VX3 = CxT2.values()['DZ']
    VITE = np.array([VX1, VX2, VX3])
    return np.transpose(VITE)


def Cal_element(point1, point2, point3, velocity):
    # because the mesh construction, the first two node cannot have same index
    a1 = Cal_orientation(point1, point2)
    a2 = Cal_orientation(point1, point3)
    ba1 = Cal_distence(point1, point2)
    ba2 = Cal_distence(point1, point3)
    normal_vector = np.cross(a1, a2) / np.linalg.norm(np.cross(a1, a2))
    if np.dot(normal_vector, velocity) < 0:
        normal_vector = -normal_vector
    surface_area = 0.5 * np.linalg.norm(np.cross(a1 * ba1, a2 * ba2))
    lift_vector = np.cross(np.cross(velocity, normal_vector), velocity) / \
                  np.linalg.norm(np.cross(np.cross(velocity, normal_vector), velocity) + 0.000000001)

    coin_alpha = abs(np.dot(normal_vector, velocity) / np.linalg.norm(velocity))
    alpha = np.arccos(coin_alpha)
    return alpha, normal_vector, lift_vector, surface_area


def FSI_mapvelocity(velocityDict, timeInFE):
    pkfile = open(velocityDict, 'rb')
    re = pickle.load(pkfile)
    pkfile.close()
    print("time in FE solver is " + str(timeInFE))
    print("time in FV solver is " + str(re['Time']))
    while float(timeInFE) > float(re['Time']):
        time.sleep(10)
        pkfile = open(velocityDict, 'rb')
        re = pickle.load(pkfile)
        pkfile.close()
    else:
        print("Now, the time in FV solver is " + str(re['Time']))
        return re['velo']
