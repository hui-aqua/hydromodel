"""
----------------------------------------------
--         University of Stavanger          --
--         Hui Cheng (PhD student)          --
--          Lin Li (Medveileder)            --
--      Prof. Muk Chen Ong (Supervisor)     --
----------------------------------------------
Any questions about this code,
please email: hui.cheng@uis.no
A module can be used to calculate the hydrodynamic forces on nets in Code_Aster.
To use this module, one should be import this into the input file for calculations.
"""
import numpy as np

row = 1025  # [kg/m3]   sea water density
kinematic_viscosity = 1.004e-6  # when the water temperature is 20 degree.
dynamic_viscosity = 1.002e-3  # when the water temperature is 20 degree.


class Net2NetWake:
    def __init__(self, model_index, node_initial_position, hydro_element, current_velocity, origin, dw0, net_solidity):
        self.positions = np.array(node_initial_position)  # a np.array for all the nodes for net, convert to numpy list
        self.elements = hydro_element  # a python list of all the elements for net
        self.flow_direction = np.array(current_velocity) / np.linalg.norm(current_velocity)
        # np.array for incoming velocity to a cage
        self.origin = np.array(origin) - np.array(current_velocity) / np.linalg.norm(current_velocity) * (
                2 * dw0 / net_solidity)
        # The coordinate of origin, it can be cage center [0,0,0]
        # (2 * dw0 / net_solidity) is a half mesh size, it is a safety factor.
        self.Sn = net_solidity
        self.wake_type = str(model_index).split("-")[0]
        self.wake_value = str(model_index).split("-")[1]
        self.wake_element_index = self.get_element_in_wake()

    def __str__(self):
        s0 = "The selected wake model is " + str(self.wake_type) + "\n"
        s1 = "The index of the element in the wake region is " + str(self.wake_element_index) + "\n"
        S = s0 + s1
        return S

    def element_in_wake(self, one_element):
        element_center = np.array([0.0, 0.0, 0.0])  # must be a float
        for node in one_element:
            element_center += np.array(self.positions[int(node)] / len(one_element))
        vector_point_to_origin = np.array(element_center - self.origin)
        if np.dot(vector_point_to_origin, self.flow_direction) < 0:
            return True
        else:
            return False

    def get_element_in_wake(self):
        element_in_wake = []
        for element in self.elements:
            if self.element_in_wake(element):
                element_in_wake.append(self.elements.index(element))
        return element_in_wake

    def reduction_factor(self, element_index, alpha=0):
        factor = 1.0
        if element_index in self.wake_element_index:
            if self.wake_type in ['factor']:
                factor = float(self.reduction_factor3())
            elif self.wake_type in ['loland']:
                factor = float(self.reduction_factor1())
            elif self.wake_type in ['hui']:
                factor = float(self.reduction_factor2(alpha))
            else:
                print("the selected wake type " + str(self.wake_type) + " is not supported.")
                print()
        else:
            factor = 1.0
        return factor

    def reduction_factor1(self):
        """
        :return: reduction factor
        """
        return 1 - 0.46 * float(self.wake_value)

    def reduction_factor2(self, alf):
        """
        :param alf: alf is the inflow angle. angle between normal vector of a net panel and flow direction
        :return: reduction factor
        """
        alf = np.abs(alf)
        reduction_factor = (np.cos(alf) + 0.05 - 0.38 * self.Sn) / (np.cos(alf) + 0.05)
        return max(0, reduction_factor)

    def reduction_factor3(self):
        """
        :return: reduction factor
        """
        return float(self.wake_value)


class HydroMorison:
    """
    For Morison hydrodynamic models, the code needs the nodes' potions \n
    and the connections.  \n
    Thus, the input variable is the matrix of nodes and the connections. \n
    In addition, the solidity and constant flow reduction are also needed.
    """

    def __init__(self, model_index, hydro_element, solidity, dwh=0.0, dw0=0.0):
        self.modelIndex = str(model_index)
        self.elements = hydro_element  # the connections of the twines[[p1,p2][p2,p3]]
        self.dwh = dwh  # used for the force calculation (reference area)
        self.dw0 = dw0  # used for the hydrodynamic coefficients
        self.Sn = solidity
        self.hydroForces_Element = np.zeros((len(self.elements), 3))

    def output_hydro_element(self):
        # return the index of the elements in the wake region
        return self.elements

    def hydro_coefficients(self, current_velocity, knot=False):
        drag_normal = 0
        drag_tangent = 0
        if self.modelIndex not in 'M1,M2,M3,M4,M5':
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
        elif self.modelIndex == 'M5':  # cifuentes 2017
            reynolds_number = row * self.dw0 * np.linalg.norm(current_velocity) / dynamic_viscosity
            drag_normal = -3.2891e-5 * pow(reynolds_number * self.Sn * self.Sn,
                                           2) + 0.00068 * reynolds_number * self.Sn * self.Sn + 1.4253
        return drag_normal, drag_tangent

    def force_on_element(self, net_wake, realtime_node_position, current_velocity, wave=0):
        """
        :param net_wake: a object wake model
        :param wave: a numpy list of wave on element, optional.
        :param realtime_node_position: a list of positions of all nodes
        :param current_velocity: np.array([ux,uy,uz]), Unit [m/s]
        :return: update the self.hydroForces_Element
        """
        if wave == 0:
            wave_velocity = np.zeros((len(self.elements), 3))
        elif len(wave) == len(self.elements):
            wave_velocity = wave
        else:
            print("The length of wave velocity is unequal ot the length of element, Please check your code.")
            exit()
        num_line = len(self.elements)
        hydro_force_on_element = []  # force on line element, initial as zeros
        for i in range(num_line):
            b = get_distance(realtime_node_position[int(self.elements[i][0])],
                             realtime_node_position[int(self.elements[i][1])])
            a = get_orientation(realtime_node_position[int(self.elements[i][0])],
                                realtime_node_position[int(self.elements[i][1])])

            velocity = np.array(current_velocity) * net_wake.reduction_factor(i) + wave_velocity[i]
            drag_n, drag_t = self.hydro_coefficients(velocity, knot=False)
            ft = 0.5 * row * self.dwh * (b - self.dwh) * drag_t * np.dot(a, velocity) * a * np.linalg.norm(
                np.dot(a, velocity))
            fn = 0.5 * row * self.dwh * (b - self.dwh) * drag_n * (velocity - np.dot(a, velocity) * a) * np.linalg.norm(
                (velocity - np.dot(a, velocity) * a))
            hydro_force_on_element.append(ft + fn)
        self.hydroForces_Element = np.array(hydro_force_on_element)
        return np.array(hydro_force_on_element)

    def distribute_force(self,number_of_node):
        """
        Transfer the forces on line element to their corresponding nodes
        :return: hydroForces_nodes
        """
        force_on_nodes = np.zeros((number_of_node, 3))  # force on nodes, initial as zeros
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

    def __init__(self, model_index, elements, solidity, dwh=0.0, dw0=0.0):
        self.modelIndex = str(model_index)
        # self.node_position = node_position  # the position matrix [[x1,y1,z1][x2,y2,z2]]
        self.hydro_element = convert_hydro_element(elements)  # the connections of the twines[[p1,p2][p2,p3]]
        self.dwh = dwh  # used for the force calculation (reference area)
        self.dw0 = dw0  # used for the hydrodynamic coefficients
        self.Sn = solidity  # solidity of th net
        self.force_on_elements = np.zeros((len(self.hydro_element), 3))

    def output_hydro_element(self):
        # return the index of the elements in the wake region
        return self.hydro_element

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

    def force_on_element(self, net_wake, realtime_node_position, current_velocity, wave=0):
        """
        :param net_wake: net2net wake model
        :param velocity_nodes: a numpy array of velocities for all nodes
        :param wave: a numpy array of wave on element, optional.
        :param realtime_node_position: a list of positions of all nodes
        :param current_velocity: numpy array ([ux,uy,uz]), Unit [m/s]
        :return:  update the self.hydroForces_Element
        """
        if wave == 0:
            wave_velocity = np.zeros((len(self.hydro_element), 3))
        elif len(wave) == len(self.hydro_element):
            wave_velocity = wave
        else:
            print("The length of wave velocity is unequal ot the length of element, Please check your code.")
            exit()
        hydro_force_on_element = []  # force on net panel, initial as zeros
        for panel in self.hydro_element:  # loop based on the hydrodynamic elements
            # velocity_structure = (velocity_nodes[panel[0]] + velocity_nodes[panel[1]] + velocity_nodes[panel[2]]) / (
            #     len(panel))
            velocity_structure = np.array([0.0, 0.0, 0.0])
            p1 = realtime_node_position[panel[0]]
            p2 = realtime_node_position[panel[1]]
            p3 = realtime_node_position[panel[2]]
            alpha, lift_direction, surface_area = calculation_on_element(p1, p2, p3, np.array(current_velocity))
            # calculate the inflow angel, normal vector, lift force factor, area of the hydrodynamic element
            velocity = np.array(current_velocity) * net_wake.reduction_factor(self.hydro_element.index(panel), alpha) + \
                       wave_velocity[self.hydro_element.index(panel)]
            # * 0.8 ** int((self.hydro_element.index(panel) + 1) / 672)
            # if not in the wake region, the effective velocity is the undisturbed velocity
            velocity_relative = velocity - velocity_structure
            drag_coefficient, lift_coefficient = self.hydro_coefficients(alpha, velocity_relative, knot=False)
            fd = 0.5 * row * surface_area * drag_coefficient * np.linalg.norm(velocity_relative) * velocity_relative
            fl = 0.5 * row * surface_area * lift_coefficient * pow(np.linalg.norm(velocity_relative),
                                                                   2) * lift_direction
            hydro_force_on_element.append((fd + fl) / 2.0)
        if np.size(np.array(hydro_force_on_element)) == np.size(self.hydro_element):
            self.force_on_elements = np.array(hydro_force_on_element)
            return np.array(hydro_force_on_element)
        else:
            print("\nError! the size of hydrodynamic force on element is not equal to the number of element."
                  "\nPlease cheack you code.")
            print("\nThe size of element is " + str(len(self.hydro_element)))
            print("\nThe size of hydrodynamic force is " + str(len(np.array(hydro_force_on_element))))
            exit()

    def screen_fsi(self, realtime_node_position, velocity_on_element, velocity_of_nodes=np.array([0, 0, 0])):
        """
        :param velocity_of_nodes: a numpy array of velocities for all nodes
        :param realtime_node_position: a numpy array of positions for all nodes
        :param velocity_on_element: a numpy array on the centers of all net panels
        :return: update the self.hydroForces_Element and output the forces on all the net panels.
        """
        # print("The length of U vector is " + str(len(velocity_on_element)))
        hydro_force_on_element = []  # force on net panel, initial as zeros
        # print("velocity elementy is 1" + str(velocity_on_element))
        # print("velocity_of_nodes is " + str(velocity_of_nodes))
        # print("realtime_node_position is " + str(realtime_node_position))
        if len(velocity_of_nodes) < len(realtime_node_position):
            velocity_of_nodes = np.zeros((len(realtime_node_position), 3))
        if len(velocity_on_element) < len(self.hydro_element):
            print("position is " + str(realtime_node_position))
            print("Velocity is " + str(velocity_of_nodes))
            print("velocity elements is " + str(velocity_on_element))
            exit()
        for panel in self.hydro_element:  # loop based on the hydrodynamic elements
            velocity_fluid = velocity_on_element[self.hydro_element.index(panel)]
            velocity_structure = (velocity_of_nodes[panel[0]] + velocity_of_nodes[panel[1]] + velocity_of_nodes[
                panel[2]]) / (len(panel))
            velocity_relative = velocity_fluid - velocity_structure * 0
            p1 = realtime_node_position[panel[0]]
            p2 = realtime_node_position[panel[1]]
            p3 = realtime_node_position[panel[2]]
            alpha, lift_direction, surface_area = calculation_on_element(p1, p2, p3, velocity_relative)
            drag_coefficient, lift_coefficient = self.hydro_coefficients(alpha, velocity_relative, knot=False)

            fd = 0.5 * row * surface_area * drag_coefficient * np.linalg.norm(np.array(velocity_relative)) * np.array(
                velocity_relative)
            fl = 0.5 * row * surface_area * lift_coefficient * pow(np.linalg.norm(velocity_relative),
                                                                   2) * lift_direction
            hydro_force_on_element.append((fd + fl) / 2.0)
        if np.size(np.array(hydro_force_on_element)) == np.size(self.hydro_element):
            self.force_on_elements = np.array(hydro_force_on_element)
            return np.array(hydro_force_on_element)
        else:
            print("Error!, the size of hydrodynamic force on element is not equal to the number of element."
                  "Please cheack you code.")
            exit()

    def distribute_velocity(self, current_velocity, wave_velocity=0):
        velocity_on_element = []  # velocity on net panel, initial as zeros
        if len(current_velocity) < 4:
            velocity_on_element = np.ones((len(self.hydro_element), 3)) * current_velocity
        elif len(current_velocity) == len(self.hydro_element):
            velocity_on_element = np.array(current_velocity)

        if not wave_velocity == 0:
            for panel in self.hydro_element:  # loop based on the hydrodynamic elements
                velocity_on_element[self.hydro_element.index(panel)] = +wave_velocity[self.hydro_element.index(panel)]
        if len(velocity_on_element) == len(self.hydro_element):
            return velocity_on_element
        else:
            print("\nError! the size of velocity on element is not equal to the number of element."
                  "\nPlease cheack you code.")
            print("\nThe size of element is " + str(len(self.hydro_element)))
            print("\nThe size of hydrodynamic force is " + str(len(velocity_on_element)))
            exit()

    def distribute_force(self, number_of_node):
        """
        Transfer the forces on net panels to their corresponding nodes
        :return: hydroForces_nodes
        """
        forces_on_nodes = np.zeros((number_of_node, 3))  # force on nodes, initial as zeros
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
    return np.transpose(position)


def get_velocity(table_aster):  # to get the velocity
    content = table_aster.EXTR_TABLE()
    velocity_x = content.values()['DX']
    velocity_y = content.values()['DY']
    velocity_z = content.values()['DZ']
    velocity = np.array([velocity_x, velocity_y, velocity_z])
    return np.transpose(velocity)


# one function used by screen model
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
    return alpha, lift_vector, surface_area


# one function used by screen model
def convert_hydro_element(elements):
    hydro_elements = []
    for panel in elements:  # loop based on the hydrodynamic elements
        if len([int(k) for k in set(panel)]) < 3:  # the hydrodynamic element is a triangle
            hydro_elements.append([k for k in set([int(k) for k in set(panel)])])  # a list of the node sequence
        else:
            for i in range(len(panel)):
                nodes = [int(k) for k in panel]  # get the list of nodes [p1,p2,p3,p4]
                nodes.pop(i)  # delete the i node to make the square to a triangle
                hydro_elements.append(nodes)  # delete the i node to make the square to a triangle
    return hydro_elements

# note:
#
# In the present program, the nodes' position is stored as numpy array not a python list for easier manipulation.
# Velocity of current and/or wave is also a numpy array.
# Element index is stored as a python list for fast running.
#
