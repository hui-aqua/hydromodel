"""
-------------------------------------------\n
-         University of Stavanger          \n
-         Hui Cheng (PhD student)          \n
-          Lin Li (Medveileder)            \n
-      Prof. Muk Chen Ong (Supervisor)     \n
-------------------------------------------\n
Any questions about this code,
please email: hui.cheng@uis.no \n
Modules can be used to calculate the hydrodynamic forces on nets.
In order to use this module, we recommend ``import hydroModels as hm`` in the beginning of your code.
Please refer to Cheng et al. (2020) [https://doi.org/10.1016/j.aquaeng.2020.102070] for details.
"""
import numpy as np

row = 1025  # [kg/m3]   sea water density
kinematic_viscosity = 1.004e-6  # when the water temperature is 20 degree.
dynamic_viscosity = 1.002e-3  # when the water temperature is 20 degree.


class forceModel:
    """
    For Morison hydrodynamic models, the forces on netting are calculated based on individual twines.
    The twines are taken as cylindrical elements. In practice, the force is usually decomposed into two componnets:
    normal drag force F_n and tangential drag force F_t (Cheng et al., 2020)
    """

    def __init__(self, model_index, hydro_element, solidity, dwh=0.0, dw0=0.0):
        """
        :param model_index: [string] Unit: [-]. To indicate the model function, e.g.: 'M1', 'M2', 'M3'.
        :param hydro_element: [list] Unit: [-]. A python list to indicate how the lines are connected.
        :param solidity: [float] Unit: [-]. The solidity of netting.
        :param dwh: [float] Unit: [m]. The hydrodynamic diameter of the numerical net twines. It is used for the force calculation (reference area)
        :param dw0: [float] Unit: [m]. The diameter of the physical net twines. It is used for the hydrodynamic coefficients.
        """
        self.modelIndex = str(model_index)
        self.elements = hydro_element  # the connections of the twines[[p1,p2][p2,p3]]
        self.dwh = dwh  # used for the force calculation (reference area)
        self.dw0 = dw0  # used for the hydrodynamic coefficients
        self.Sn = solidity
        self.hydroForces_Element = np.zeros((len(self.elements), 3))

    def output_hydro_element(self):
        """
        :return: [list] Unit: [-]. A list of indexes of the elements in the wake region.
        """
        return self.elements

    def hydro_coefficients(self, current_velocity):
        """
        :param current_velocity: [np.array].shape=(1,3) Unit: [m/s]. The current velocity [ux,uy,uz] in cartesian coordinate system.
        :return: normal and tangential drag force coefficients. [float] Unit: [-].
        """
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

    def force_on_element(self, net_wake, realtime_node_position, current_velocity, wave=False, fe_time=0):
        """
        :param net_wake: A object wake model, net2net wake model. Must create first.
        :param realtime_node_position: [np.array].shape=(N,3) Unit: [m]. The coordinates of N nodes in cartesian coordinate system.
        :param current_velocity: [np.array].shape=(1,3) Unit [m/s]. The current velocity [ux,uy,uz] in cartesian coordinate system.
        :param wave:  A wake model object. *Default value=False* Must create first.
        :param fe_time: [float] Unit [s]. The time in Code_Aster. *Default value=0* Must give if wave is added.
        :param current_velocity: numpy array ([ux,uy,uz]), Unit [m/s]
        :return: [np.array].shape=(M,3) Unit [N]. The hydrodynamic forces on all M elements. Meanwhile, update the self.hydroForces_Element
        """
        num_line = len(self.elements)
        hydro_force_on_element = []  # force on line element, initial as zeros
        wave_velocity = np.zeros((num_line, 3))
        if wave:
            for index,line in enumerate(self.elements):
                element_center = (realtime_node_position[int(line[0])] + realtime_node_position[int(line[1])]) / 2.0
                wave_velocity[index] = wave.get_velocity(element_center, fe_time)

        for i in range(num_line):
            b = get_distance(realtime_node_position[int(self.elements[i][0])],
                             realtime_node_position[int(self.elements[i][1])])
            a = get_orientation(realtime_node_position[int(self.elements[i][0])],
                                realtime_node_position[int(self.elements[i][1])])

            velocity = np.array(current_velocity) * net_wake.reduction_factor(i) + wave_velocity[i]
            drag_n, drag_t = self.hydro_coefficients(velocity)
            ft = 0.5 * row * self.dwh * (b - self.dwh) * drag_t * np.dot(a, velocity) * a * np.linalg.norm(
                np.dot(a, velocity))
            fn = 0.5 * row * self.dwh * (b - self.dwh) * drag_n * (velocity - np.dot(a, velocity) * a) * np.linalg.norm(
                (velocity - np.dot(a, velocity) * a))
            hydro_force_on_element.append(ft + fn)
        self.hydroForces_Element = np.array(hydro_force_on_element)
        return np.array(hydro_force_on_element)

    def distribute_force(self, number_of_node):
        """
        Transfer the forces on line element to their corresponding nodes.\n
        :return: [np.array].shape=(N,3) Unit [N]. The hydrodynamic forces on all N nodes
        """
        force_on_nodes = np.zeros((number_of_node, 3))  # force on nodes, initial as zeros
        for index, line in enumerate(self.elements):
            force_on_nodes[line[0]] += (self.hydroForces_Element[index]) / 2
            force_on_nodes[line[1]] += (self.hydroForces_Element[index]) / 2
        return force_on_nodes

def get_distance(p1, p2):
    """
    Module private function.\n
    :param p1: point1 [np.array].shape=(1,3) or a [list] of coordinates Unit: [m].
    :param p2: point2 [np.array].shape=(1,3) or a [list] of coordinates Unit: [m].
    :return: The distance between two points.  [float] Unit [m].
    """

    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    dz = p2[2] - p1[2]
    return np.sqrt(dx ** 2 + dy ** 2 + dz ** 2)


def get_orientation(p1, p2):
    """
    Module private function.\n
    :param p1: point1 [np.array].shape=(1,3) or a [list] of coordinates Unit: [m].
    :param p2: point2 [np.array].shape=(1,3) or a [list] of coordinates Unit: [m].
    :return: The unit vector from p1 to p2.
    """
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    dz = p2[2] - p1[2]
    p = np.array([dx, dy, dz])
    return p / np.linalg.norm(p)

# note:
#
# In the present program, the nodes' position is stored as numpy array not a python list for easier manipulation.
# Velocity of current and/or wave is also a numpy array.
# Element index is stored as a python list for fast running.
#
