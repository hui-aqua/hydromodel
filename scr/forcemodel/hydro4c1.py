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
kinematic_viscosity = 1.004e-6  # when the water temperature is 20 degree.
dynamic_viscosity = 1.002e-3  # when the water temperature is 20 degree.


class Net2NetWake:
    def __init__(self, node_position, hydro_element, current_velocity, net_solidity):
        self.positions = node_position  # a list of all the nodes for net
        self.elements = hydro_element  # a list of all the elements for net
        self.U = current_velocity  # incoming velocity for cage
        self.cage_center = np.array([0, 0, 0])  # set the cage center is [0,0,0]
        self.Sn = net_solidity

    def get_element_in_wake(self):
        element_in_wake = []
        for i in range(len(self.elements)):
            for j in range(len(self.elements[i])):
                x = 0
                y = 0
                z = 0
                x += self.positions[self.elements[i][j]][0] / len(self.elements[i])
                y += self.positions[self.elements[i][j]][1] / len(self.elements[i])
                z += self.positions[self.elements[i][j]][2] / len(self.elements[i])
            vector_point_to_cage_center = (np.array([x, y, z]) - self.cage_center)
            if np.dot(vector_point_to_cage_center, self.U) < 0:
                element_in_wake.append(i)
        return element_in_wake

    def reduction_factor2(self, alf):  # alf is the inflow angle
        alf = np.abs(alf)
        reduction_factor = (np.cos(alf) + 0.05 - 0.38 * self.Sn) / (np.cos(alf) + 0.05)
        return max(0, reduction_factor)

    def reduction_factor1(self):  # alf is the inflow angle
        cd = 0.04 + (-0.04 + 0.33 * self.Sn + 6.54 * pow(self.Sn, 2) - 4.88 * pow(self.Sn, 3))
        return 1 - 0.46 * cd


class HydroMorison:
    """
    For Morison hydrodynamic models, the code needs the nodes' potions \n
    and the connections.  \n
    Thus, the input variable is the matrix of nodes and the connections. \n
    In addition, the solidity and constant flow reduction are also needed.
    """

    def __init__(self, model_index, position_matrix, hydro_element, solidity, current_direction, dwh=0.0, dw0=0.0):
        self.modelIndex = str(model_index)
        self.positions = position_matrix  # the position matrix [[x1,y1,z1][x2,y2,z2]]
        self.elements = hydro_element  # the connections of the twines[[p1,p2][p2,p3]]
        self.dwh = dwh  # used for the force calculation (reference area)
        # can be a consistent number or a list
        self.dw0 = dw0  # used for the hydrodynamic coefficients
        # can be a consistent number or a list
        self.Sn = solidity
        wake = Net2NetWake(self.positions, self.elements, current_direction, self.Sn)
        self.ref = wake.get_element_in_wake()
        self.hydroForces_Element = np.zeros((len(self.elements), 3))

    def output_element_in_wake(self):
        return self.ref

    def hydro_coefficients(self, current_velocity, knot=False):
        drag_normal = 0
        drag_tangent = 0
        if self.modelIndex not in 'S1,S2,S3,S4,S5,S6':
            print("The selected hydrodynamic model is not included in the present program")
            exit()
        elif self.modelIndex == 'M1':  # Bessonneau 1998
            drag_normal = 1.2
            drag_tangent = 0.1
        elif self.modelIndex == 'M2':  # Wan 2002
            drag_normal = 1.3
            drag_tangent = 0.0
        elif self.modelIndex == 'M3':  # Takagi 2004
            reynolds_number = row * self.dw0 * np.linalg.norm(current_velocity) / dynamic_viscosity
            if reynolds_number < 200:
                drag_normal = pow(10, 0.7) * pow(reynolds_number, -0.3)
            else:
                drag_normal = 1.2
            drag_tangent = 0.1
        elif self.modelIndex == 'M4':  # choo 1971
            reynolds_number = row * self.dw0 * np.linalg.norm(current_velocity) / dynamic_viscosity
            drag_tangent = np.pi * dynamic_viscosity * (
                    0.55 * np.sqrt(reynolds_number) + 0.084 * pow(reynolds_number, 2.0 / 3.0))
            s = -0.07721565 + np.log(8.0 / reynolds_number)
            if 0 < reynolds_number < 1:
                drag_normal = 8 * np.pi * (1 - 0.87 * pow(s, -2)) / (s * reynolds_number)
            elif reynolds_number < 30:
                drag_normal = 1.45 + 8.55 * pow(reynolds_number, -0.9)
            elif reynolds_number < 2.33e5:
                drag_normal = 1.1 + 4 * pow(reynolds_number, -0.5)
            elif reynolds_number < 4.92e5:
                drag_normal = (-3.41e-6) * (reynolds_number - 5.78e5)
            elif reynolds_number < 1e7:
                drag_normal = 0.401 * (1 - np.exp(-reynolds_number / 5.99 * 1e5))
            else:
                print("Reynold number=" + str(reynolds_number) + ", and it exceeds the range.")
                exit()
        return drag_normal, drag_tangent

    def force_on_element(self, realtime_node_position, current_velocity):
        """
        :param realtime_node_position: a list of positions of all nodes
        :param current_velocity: [ux,uy,uz], Unit [m/s]
        :return: update the self.hydroForces_Element
        """
        num_line = len(self.elements)
        hydro_force_on_element = []  # force on line element, initial as zeros
        for i in range(num_line):
            b = get_distance(realtime_node_position[int(self.elements[i][0])],
                             realtime_node_position[int(self.elements[i][1])])
            a = get_orientation(realtime_node_position[int(self.elements[i][0])],
                                realtime_node_position[int(self.elements[i][1])])
            if i in self.ref:
                velocity = 0.8 * np.array(current_velocity)
            else:
                velocity = np.array(current_velocity)
            drag_n, drag_t = self.hydro_coefficients(current_velocity, knot=False)
            ft = 0.5 * row * self.dwh * (b - self.dwh) * drag_t * np.dot(a, velocity) * a * np.linalg.norm(
                np.dot(a, velocity))
            fn = 0.5 * row * self.dwh * (b - self.dwh) * drag_n * (velocity - np.dot(a, velocity) * a) * np.linalg.norm(
                (velocity - np.dot(a, velocity) * a))
            hydro_force_on_element.append(ft + fn)
        self.hydroForces_Element = np.array(hydro_force_on_element)

    def distribute_force(self):
        """
        Transfer the forces on line element to their corresponding nodes
        :return: hydroForces_nodes
        """
        force_on_nodes = np.zeros((len(self.positions), 3))  # force on nodes, initial as zeros
        for line in self.elements:
            force_on_nodes[line[0]] += (self.hydroForces_Element[self.elements.index(line)]) / 2
            force_on_nodes[line[1]] += (self.hydroForces_Element[self.elements.index(line)]) / 2
        return force_on_nodes


class HydroScreen:
    """
    For Screen hydrodynamic models, the code needs the panel' potions \n
    and the connections.  \n
    Thus, the input variable is the matrix of nodes and the connetions. \n
    In addition, the solidity and constant flow reduction are also needed.
    """

    def __init__(self, model_index, node_position, elements, solidity, current_direction, dwh=0.0, dw0=0.0):
        self.modelIndex = str(model_index)
        self.node_position = node_position  # the position matrix [[x1,y1,z1][x2,y2,z2]]
        self.hydro_element = self.convert_hydro_element(elements)  # the connections of the twines[[p1,p2][p2,p3]]
        self.dwh = dwh  # used for the force calculation (reference area)
        self.dw0 = dw0  # used for the hydrodynamic coefficients
        self.Sn = solidity  # solidity of th net
        self.wake = Net2NetWake(self.node_position, self.hydro_element, current_direction,
                                self.Sn)  # create wake object
        self.ref = self.wake.get_element_in_wake()  # get the elements in the wake
        self.force_on_elements = np.zeros((len(self.hydro_element), 3))

    def output_element_in_wake(self):
        # return the index of the elements in the wake region
        return self.ref

    def output_hydro_element(self):
        # return the index of the elements in the wake region
        return self.hydro_element

    def convert_hydro_element(self, elements):
        hydro_elements = []
        for panel in elements:  # loop based on the hydrodynamic elements
            if len([int(k) for k in set(panel)]) == 3:  # the hydrodynamic element is a triangle
                hydro_elements.append([k for k in set([int(k) for k in set(panel)])])  # a list of the node sequence
            else:
                for i in range(len(panel)):  # loop 4 times to map the force
                    nodes = [int(k) for k in panel]  # get the list of nodes [p1,p2,p3,p4]
                    nodes.pop(i)  # delete the i node to make the square to a triangle
                    hydro_elements.append(nodes)  # delete the i node to make the square to a triangle
        return hydro_elements

    def hydro_coefficients(self, inflow_angle, current_velocity, knot=False):
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
            reynolds_number = row * self.dw0 * np.linalg.norm(current_velocity) / dynamic_viscosity / (
                    1 - self.Sn)  # Re
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
            reynolds_number = np.linalg.norm(current_velocity) * self.dw0 * row / dynamic_viscosity
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
            reynolds_cylinder = row * self.dw0 * np.linalg.norm(current_velocity) / dynamic_viscosity / (
                    1 - self.Sn) + 0.000001
            cd_cylinder = 1 + 10.0 / (pow(reynolds_cylinder, 2.0 / 3.0))
            drag_coefficient = cd_cylinder * (0.12 - 0.74 * self.Sn + 8.03 * pow(self.Sn, 2)) * pow(inflow_angle, 3)
            if knot:
                mesh_size = 10 * self.dw0  # assume Sn=0.2
                diameter_knot = 2 * self.dw0  # assume the knot is twice of the diameter of the twine
                reynolds_sphere = row * diameter_knot * np.linalg.norm(current_velocity) / dynamic_viscosity / (
                        1 - self.Sn) + 0.000001
                coe_sphere = 24.0 / reynolds_sphere + 6.0 / (1 + np.sqrt(reynolds_sphere)) + 0.4
                drag_coefficient = (cd_cylinder * 8 * pow(diameter_knot,
                                                          2) + coe_sphere * np.pi * mesh_size * self.dw0) / np.pi * mesh_size * self.dw0 * (
                                           0.12 - 0.74 * self.Sn + 8.03 * pow(self.Sn, 2)) * pow(inflow_angle, 3)
            else:
                pass
        return drag_coefficient, lift_coefficient

    def force_on_element(self, realtime_node_position, current_velocity):
        """
        :param realtime_node_position: a list of positions of all nodes
        :param current_velocity: [ux,uy,uz], Unit [m/s]
        :return:  update the self.hydroForces_Element
        """
        hydro_force_on_element = []  # force on net panel, initial as zeros
        for panel in self.hydro_element:  # loop based on the hydrodynamic elements
            p1 = realtime_node_position[panel[0]]
            p2 = realtime_node_position[panel[1]]
            p3 = realtime_node_position[panel[2]]
            alpha, drag_direction, lift_direction, surface_area = calculation_on_element(p1, p2, p3, current_velocity)
            # calculate the inflow angel, normal vector, lift force factor, area of the hydrodynamic element
            # set([int(k) for k in set(panel)])   # get a set of the node sequence in the element
            if self.hydro_element.index(panel) in self.ref:  # if the element in the wake region
                velocity = current_velocity * self.wake.reduction_factor2(alpha)
            else:
                velocity = current_velocity
                # * 0.8 ** int((self.hydro_element.index(panel) + 1) / 672)
                # if not in the wake region, the effective velocity is the undisturbed velocity

            drag_coefficient, lift_coefficient = self.hydro_coefficients(alpha, velocity, knot=False)
            fd = 0.5 * row * surface_area * drag_coefficient * np.linalg.norm(velocity) * velocity
            fl = 0.5 * row * surface_area * lift_coefficient * pow(np.linalg.norm(velocity), 2) * lift_direction
            hydro_force_on_element.append((fd + fl) / 2.0)
        if np.size(np.array(hydro_force_on_element)) == np.size(self.hydro_element):
            self.force_on_elements = np.array(hydro_force_on_element)
        else:
            print("\nError! the size of hydrodynamic force on element is not equal to the number of element."
                  "\nPlease cheack you code.")
            print("\nThe size of element is " + str(len(self.hydro_element)))
            print("\nThe size of hydrodynamic force is " + str(len(np.array(hydro_force_on_element))))
            exit()

    def screen_fsi(self, realtime_node_position, velocity_on_element):
        """
        :param realtime_node_position: a list of positions of all nodes
        :param velocity_on_element: a list of velocity on the centers of all net panels
        :return: update the self.hydroForces_Element and output the forces on all the net panels.
        """
        print("The length of U vector is " + str(len(velocity_on_element)))
        hydro_force_on_element = []  # force on net panel, initial as zeros
        for panel in self.hydro_element:  # loop based on the hydrodynamic elements
            velocity = velocity_on_element[self.hydro_element.index(panel)]
            p1 = realtime_node_position[panel[0]]
            p2 = realtime_node_position[panel[1]]
            p3 = realtime_node_position[panel[2]]
            alpha, drag_direction, lift_direction, surface_area = calculation_on_element(p1, p2, p3, velocity)
            drag_coefficient, lift_coefficient = self.hydro_coefficients(alpha, velocity, knot=False)
            fd = 0.5 * row * surface_area * drag_coefficient * np.linalg.norm(np.array(velocity)) * np.array(velocity)
            fl = 0.5 * row * surface_area * lift_coefficient * pow(np.linalg.norm(velocity), 2) * lift_direction
            hydro_force_on_element.append((fd + fl) / 2.0)
        if np.size(np.array(hydro_force_on_element)) == np.size(self.hydro_element):
            self.force_on_elements = np.array(hydro_force_on_element)
            return np.array(hydro_force_on_element)
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


# - five functions used in the current file
def get_distance(p1, p2):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    dz = p2[2] - p1[2]
    return np.sqrt(dx ** 2 + dy ** 2 + dz ** 2)


def get_orientation(p1, p2):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    dz = p2[2] - p1[2]
    p = np.array([dx, dy, dz])
    return p / np.linalg.norm(p)


# two function used by code_aster
# ## to get the position ##########################################
def get_position(table_aster):
    content = table_aster.EXTR_TABLE()
    original_x = content.values()['COOR_X']
    original_y = content.values()['COOR_Y']
    original_z = content.values()['COOR_Z']
    delta_x = content.values()['DX']
    delta_y = content.values()['DY']
    delta_z = content.values()['DZ']
    position = np.array([original_x, original_y, original_z]) + np.array([delta_x, delta_y, delta_z])
    # print('In hy, the posi is'+str(np.transpose(POSI)))
    return np.transpose(position)


def get_velocity(table_aster):  # to get the velocity
    content = table_aster.EXTR_TABLE()
    velocity_x = content.values()['DX']
    velocity_y = content.values()['DY']
    velocity_z = content.values()['DZ']
    velocity = np.array([velocity_x, velocity_y, velocity_z])
    return np.transpose(velocity)


def calculation_on_element(point1, point2, point3, velocity):
    # because the mesh construction, the first two node cannot have same index
    a1 = get_orientation(point1, point2)
    a2 = get_orientation(point1, point3)
    ba1 = get_distance(point1, point2)
    ba2 = get_distance(point1, point3)
    normal_vector = np.cross(a1, a2) / np.linalg.norm(np.cross(a1, a2))
    if np.dot(normal_vector, velocity) < 0:
        normal_vector = -normal_vector
    surface_area = 0.5 * np.linalg.norm(np.cross(a1 * ba1, a2 * ba2))
    lift_vector = np.cross(np.cross(velocity, normal_vector), velocity) / \
                  np.linalg.norm(np.cross(np.cross(velocity, normal_vector), velocity) + 0.000000001)

    coin_alpha = abs(np.dot(normal_vector, velocity) / np.linalg.norm(velocity))
    alpha = np.arccos(coin_alpha)
    return alpha, normal_vector, lift_vector, surface_area


def fsi_velocity_mapping(velocity_foam, time_aster):
    pk_file = open(velocity_foam, 'rb')
    re = pickle.load(pk_file)
    pk_file.close()
    print("time in FE solver is " + str(time_aster))
    print("time in FV solver is " + str(re['Time']))
    while float(time_aster) > float(re['Time']):
        time.sleep(10)
        pk_file = open(velocity_foam, 'rb')
        re = pickle.load(pk_file)
        pk_file.close()
    else:
        print("Now, the time in FV solver is " + str(re['Time']))
        return re['velo']
