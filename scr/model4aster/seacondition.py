"""
-------------------------------------------\n
-         University of Stavanger          \n
-         Hui Cheng (PhD student)          \n
-          Lin Li (Medveileder)            \n
-      Prof. Muk Chen Ong (Supervisor)     \n
-------------------------------------------\n
Any questions about this code,
please email: hui.cheng@uis.no \n
A module can be used to provide the wave velocity
In order to use this module, we recommend ``import seacondition as sc`` in the beginning of your code.

    .. note:: In this library, I assume the wave is coming from -X, and long X-axis, Z is the gravity direction,Z=0 is the water level, and the water is below z=0.

reference: 2000linearwavetheory_NTNU.pdf
"""
import numpy as np
from numpy import pi


class Airywave:
    """
    Using Airy wave theory      \n
    """
    def __init__(self, waveHeight=1.0, waveLength=25.0, waterDepth=60.0):
        """
        :param waveHeight: [float] Unit: [m]. wave height.
        :param waveLength: [float] Unit: [m]. wavelength.
        :param waterDepth: [float] Unit: [m]. water depth.
        """
        self.gravity = 9.81
        self.waveHeight = waveHeight
        self.waveLength = waveLength
        self.waterDepth = waterDepth
        self.phasevelocity = np.sqrt(self.gravity * waveLength * np.tanh(2 * pi * waterDepth / waveLength) / (2.0 * pi))
        self.wavePeriod = waveLength / self.phasevelocity
        self.wavek = 2 * pi / waveLength
        self.piht = pi * waveHeight / self.wavePeriod
        self.pihl = pi * waveHeight / waveLength
        self.piht2 = 2 * waveHeight * pow(pi / self.wavePeriod, 2)

    def __str__(self):
        s0 = 'The environment is airy wave (deep water) wave condition and the specific parameters are:\n'
        s1 = 'water Depth= ' + str(self.waterDepth) + ' m\n'
        s2 = 'wave Period= ' + str(self.wavePeriod) + ' s\n'
        s3 = 'wave Length= ' + str(self.waveLength) + ' m\n'
        s4 = 'wave Height= ' + str(self.waveHeight) + ' m\n'
        S = s0 + s1 + s2 + s3 + s4
        return S

    def get_velocity(self, posi, time):
        """
        :param posi: [np.array].shape=(1,3) or a [list] of coordinates Unit: [m]. The position of the point which you want to know the wave velocity
        :param time: [float] Unit: [s]. The time which you want to know the wave velocity
        :return:  [np.array].shape=(1,3) Unit: [m/s]. A numpy array of the velocity at the targeted point.
        """
        zeta = self.wavek * posi[0] - 2 * pi / self.wavePeriod * time
        yita = self.get_surface(posi, time)
        if posi[2] < yita:
            horizonvelocity = self.piht * np.cosh(self.wavek * (posi[2] + self.waterDepth)) * np.cos(zeta) / np.sinh(
                self.wavek * self.waterDepth)
            vericalvelocity = self.piht * np.sinh(self.wavek * (posi[2] + self.waterDepth)) * np.sin(zeta) / np.sinh(
                self.wavek * self.waterDepth)

            if self.waterDepth > self.waveLength * 0.5:  # if it is deep water
                print("here")
                horizonvelocity = self.piht * np.exp(self.wavek * posi[2]) * np.cos(zeta)
                vericalvelocity = self.piht * np.exp(self.wavek * posi[2]) * np.sin(zeta)
        else:
            horizonvelocity = 0.0
            vericalvelocity = 0.0
        velo = np.array([0.0, 0.0, 0.0])
        velo[0] = horizonvelocity
        velo[1] = 0.0
        velo[2] = vericalvelocity
        return velo

    def get_acceleration(self, posi, time):
        """
        :param posi: [np.array].shape=(1,3) or a [list] of coordinates Unit: [m]. The position of the point which you want to know the wave acceleration.
        :param time: [float] Unit: [s]. The time which you want to know the wave velocity
        :return: [np.array].shape=(1,3) Unit: [m/s]. A numpy array of the acceleration at the targeted point.
        """

        zeta = self.wavek * posi[0] - 2 * pi / self.wavePeriod * time
        yita = self.get_surface(posi, time)
        if posi[2] < yita:
            horizontalacceleration = self.piht2 * np.cosh(self.wavek * (posi[2] + self.waterDepth)) * np.sin(
                zeta) / np.sinh(self.wavek * self.waterDepth)
            vericalaccelateration = -self.piht2 * np.sinh(self.wavek * (posi[2] + self.waterDepth)) * np.cos(
                zeta) / np.sinh(self.wavek * self.waterDepth)
            if self.waterDepth > self.waveLength * 0.5:  # if it is deep water
                horizontalacceleration = self.piht2 * np.exp(self.wavek * posi[2]) * np.sin(zeta)
                vericalaccelateration = -self.piht2 * np.exp(self.wavek * posi[2]) * np.cos(zeta)
        else:
            horizontalacceleration = 0.0
            vericalaccelateration = 0.0
        acce = np.array([0.0, 0.0, 0.0])
        acce[0] = horizontalacceleration
        acce[1] = 0.0
        acce[2] = vericalaccelateration
        return acce

    def get_surface(self, positions, time):
        """
        A class private function
        :param positions: [np.array].shape=(1,3) or a [list] of coordinates Unit: [m]. The position of the point which you want to know the wave velocity or acceleration.
        :param time: [float] Unit: [s].
        :return: [float] Unit: [m]. The sea surface level in Z direction. At the targeted position.
        """
        zeta = self.wavek * positions[0] - 2 * pi / self.wavePeriod * time
        yita = self.waveHeight / 2 * np.cos(zeta)
        return yita

    def get_velocity_at_nodes(self, list_of_point, global_time):
        """
        Get a list of velocity at a list of point
        """
        list_of_velocity = []
        for point in list_of_point:
            velocity_at_point = self.get_velocity(point, global_time)
            list_of_velocity.append(velocity_at_point)
        return list_of_velocity

    def get_velocity_at_elements(self, position_nodes, elements, global_time):
        """
        :param position_nodes: a numpy list of position \n
        :param elements: a python list of element \n
        :param global_time: time [s] \n
        :return: Get a numpy array of velocity at a list of elements \n
        """
        velocity_list = []
        for element in elements:
            element_center = np.array([0, 0, 0])
            for node in element:
                element_center += position_nodes[node] / len(element)
            velocity_on_element = self.get_velocity(element_center, global_time)
            velocity_list.append(velocity_on_element)
        return np.array(velocity_list)


class Stocks2wave(Airywave):
    def __str__(self):
        s0 = 'The environment is stokes second order wave theory condition and the specific parameters are:\n'
        s1 = 'water Depth= ' + str(self.waterDepth) + ' m\n'
        s2 = 'wave Period= ' + str(self.wavePeriod) + ' s\n'
        s3 = 'wave Length= ' + str(self.waveLength) + ' m\n'
        s4 = 'wave Height= ' + str(self.waveHeight) + ' m\n'
        S = s0 + s1 + s2 + s3 + s4
        return S

    def get_velocity(self, posi, time):
        zeta = self.wavek * posi[0] - 2 * pi / self.wavePeriod * time
        yita = self.get_surface(posi, time)
        if posi[2] < yita:
            horizonvelocity = self.piht * np.cosh(self.wavek * (posi[2] + self.waterDepth)) * np.cos(zeta) / np.sinh(
                self.wavek * self.waterDepth) + 0.75 * self.piht * self.pihl * np.cosh(
                2 * self.wavek * (posi[2] + self.waterDepth)) * np.cos(2 * zeta) / pow(4, np.sinh(
                self.wavek * self.waterDepth))
            vericalvelocity = self.piht * np.sinh(self.wavek * (posi[2] + self.waterDepth)) * np.sin(zeta) / np.sinh(
                self.wavek * self.waterDepth) + 0.75 * self.piht * self.pihl * np.sinh(
                2 * self.wavek * (posi[2] + self.waterDepth)) * np.sin(2 * zeta) / pow(4, np.sinh(
                self.wavek * self.waterDepth))
            if self.waterDepth > self.waveLength * 0.5:  # if it is deep water
                horizonvelocity = self.piht * np.exp(self.wavek * posi[2]) * np.cos(
                    zeta) + 0.75 * self.piht * self.pihl * np.cosh(
                    2 * self.wavek * (posi[2] + self.waterDepth)) * np.cos(2 * zeta) / pow(4, np.sinh(
                    self.wavek * self.waterDepth))
                vericalvelocity = self.piht * np.exp(self.wavek * posi[2]) * np.sin(
                    zeta) + 0.75 * self.piht * self.pihl * np.sinh(
                    2 * self.wavek * (posi[2] + self.waterDepth)) * np.sin(2 * zeta) / pow(4, np.sinh(
                    self.wavek * self.waterDepth))
        else:
            horizonvelocity = 0.0
            vericalvelocity = 0.0
        velo = np.array([0.0, 0.0, 0.0])
        velo[0] = horizonvelocity
        velo[1] = 0.0
        velo[2] = vericalvelocity
        return velo

    def get_acceleration(self, posi, time):
        zeta = self.wavek * posi[0] - 2 * pi / self.wavePeriod * time
        yita = self.get_surface(posi, time)
        if posi[2] < yita:
            horizontalacceleration = self.piht2 * np.cosh(self.wavek * (posi[2] + self.waterDepth)) * np.sin(
                zeta) / np.sinh(self.wavek * self.waterDepth) + 1.5 * self.piht2 * self.pihl * np.cosh(
                2 * self.wavek * (posi[2] + self.waterDepth)) * np.sin(2 * zeta) / pow(4, np.sinh(
                self.wavek * self.waterDepth))
            vericalaccelateration = -self.piht2 * np.sinh(self.wavek * (posi[2] + self.waterDepth)) * np.cos(
                zeta) / np.sinh(self.wavek * self.waterDepth) - 1.5 * self.piht2 * self.pihl * np.sinh(
                2 * self.wavek * (posi[2] + self.waterDepth)) * np.cos(2 * zeta) / pow(4, np.sinh(
                self.wavek * self.waterDepth))
            if self.waterDepth > self.waveLength * 0.5:  # if it is deep water
                horizontalacceleration = self.piht2 * np.exp(self.wavek * posi[2]) * np.sin(
                    zeta) + 1.5 * self.piht2 * self.pihl * np.cosh(
                    2 * self.wavek * (posi[2] + self.waterDepth)) * np.sin(2 * zeta) / pow(4, np.sinh(
                    self.wavek * self.waterDepth))
                vericalaccelateration = -self.piht2 * np.exp(self.wavek * posi[2]) * np.cos(
                    zeta) - 1.5 * self.piht2 * self.pihl * np.sinh(
                    2 * self.wavek * (posi[2] + self.waterDepth)) * np.cos(2 * zeta) / pow(4, np.sinh(
                    self.wavek * self.waterDepth))
        else:
            horizontalacceleration = 0.0
            vericalaccelateration = 0.0
        acce = np.array([0.0, 0.0, 0.0])
        acce[0] = horizontalacceleration
        acce[1] = 0.0
        acce[2] = vericalaccelateration
        return acce

    def get_surface(self, posi, time):
        zeta = self.wavek * posi[0] - 2 * pi / self.wavePeriod * time
        yita = self.waveHeight / 2 * np.cos(
            zeta) + pi * self.waveHeight * self.waveHeight / 8.0 / self.waveLength * np.cosh(
            self.wavek * self.waterDepth) * (2 + np.cosh(2 * self.wavek * self.waterDepth)) * np.cos(2 * zeta) / pow(
            np.sinh(self.wavek * self.waterDepth), 3)
        return yita
