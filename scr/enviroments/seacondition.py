"""
/--------------------------------\
|    University of Stavanger     |
|           Hui Cheng            |
\--------------------------------/
Any questions about this code, please email: hui.cheng@uis.no
A module can be used to calculate the hydrodynamic forces on nets in Code_Aster.
To use this module, one should be import this into the input file for calculations.

In this library, I assume the wave is coming from -X, and long X-axis,
Z is the gravity direction,Z=0 is the water level, and the water is below z=0
reference:2000linearwavetheory_NTNU.pdf
"""
import numpy as np
from numpy import pi


class Airywave:
    """
    Using Airy wave theory      \n
    To define this class, need to import:    \n
    waveheight [m], wavelength [m], waveperiod [s], waterdepth [m] \n
    in this library, I assume the wave is coming from -X, and long X-axis,
    Z is the gravity direction,Z=0 iz the water level, and the water is below z=0
    If there are any questions, please contact hui.cheng@uis.no
    """

    def __init__(self, waveHeight=1.0, waveLength=25.0, waterDepth=60.0):
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

    def Get_Velo(self, posi, time):
        zeta = self.wavek * posi[0] - 2 * pi / self.wavePeriod * time
        yita = self.Get_Surface(posi, time)
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

    def Get_Acce(self, posi, time):
        zeta = self.wavek * posi[0] - 2 * pi / self.wavePeriod * time
        yita = self.Get_Surface(posi, time)
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

    def Get_Surface(self, posi, time):
        zeta = self.wavek * posi[0] - 2 * pi / self.wavePeriod * time
        yita = self.waveHeight / 2 * np.cos(zeta)
        return yita

    def Get_posiVelos(self, listofpoint, Golbaltime):
        '''
        Get a list of velocity at a list of point
        '''
        listOfVelo = []
        for point in listofpoint:
            velocityAtPoint = self.Get_Velo(point, Golbaltime)
            listOfVelo.append(velocityAtPoint)
        return listOfVelo

    def Get_elemVelos(self, listofpoint, listofelement, Golbaltime):
        '''
        Get a list of velocity at a list of element
        '''
        listOfveloatElem = []
        for element in listofelement:
            lenngthofelement = len(element)
            xs, ys, zs = 0, 0, 0
            for point in element:
                xs += listofpoint[point][0]
                ys += listofpoint[point][1]
                zs += listofpoint[point][2]
            centerP = [xs / lenngthofelement, ys / lenngthofelement, zs / lenngthofelement, ]
            velocityAtPoint = self.Get_Velo(centerP, Golbaltime)
            listOfveloatElem.append(velocityAtPoint)
        return listOfveloatElem


class Stocks2wave(Airywave):
    def __str__(self):
        s0 = 'The environment is stokes second order wave theory condition and the specific parameters are:\n'
        s1 = 'water Depth= ' + str(self.waterDepth) + ' m\n'
        s2 = 'wave Period= ' + str(self.wavePeriod) + ' s\n'
        s3 = 'wave Length= ' + str(self.waveLength) + ' m\n'
        s4 = 'wave Height= ' + str(self.waveHeight) + ' m\n'
        S = s0 + s1 + s2 + s3 + s4
        return S

    def Get_Velo(self, posi, time):
        zeta = self.wavek * posi[0] - 2 * pi / self.wavePeriod * time
        yita = self.Get_Surface(posi, time)
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

    def Get_Acce(self, posi, time):
        zeta = self.wavek * posi[0] - 2 * pi / self.wavePeriod * time
        yita = self.Get_Surface(posi, time)
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

    def Get_Surface(self, posi, time):
        zeta = self.wavek * posi[0] - 2 * pi / self.wavePeriod * time
        yita = self.waveHeight / 2 * np.cos(
            zeta) + pi * self.waveHeight * self.waveHeight / 8.0 / self.waveLength * np.cosh(
            self.wavek * self.waterDepth) * (2 + np.cosh(2 * self.wavek * self.waterDepth)) * np.cos(2 * zeta) / pow(
            np.sinh(self.wavek * self.waterDepth), 3)
        return yita
