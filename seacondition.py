# writer: hui.cheng@uis.no
# please contact the writer if there is any questions
import numpy as np
from numpy import pi


class IdeLinwave:
    """
    Using idealized linear waves theory\n
    To define this class, need to import:\n
    waveheight [m], wavelength [m], waveperiod [s], waterdepth [m]\n
    If there are any questions, please contact hui.cheng@uis.no
    """

    def __init__(self, waveHeight=1.0,
                 waveLength=25.0,
                 #  wavePeriod=4.0,
                 waterDepth=60.0):
        self.waveHeight = waveHeight
        self.waveLength = waveLength
        self.wavePeriod = np.sqrt(2 * pi * waveLength / 9.81)
        self.waterDepth = waterDepth

    def __str__(self):
        s0 = 'The environment is idealized linear wave condition and the specific parameters are:\n'
        s1 = 'water Depth= ' + str(self.waterDepth) + ' m\n'
        s2 = 'wave Period= ' + str(self.wavePeriod) + ' s\n'
        s3 = 'wave Length= ' + str(self.waveLength) + ' m\n'
        s4 = 'wave Height= ' + str(self.waveHeight) + ' m\n'

        S = s0 + s1 + s2 + s3 + s4
        return S

    def Get_Velo(self, posi, time):
        wavek = 2 * np.pi / self.waveLength
        piht = np.pi * self.waveHeight / self.wavePeriod
        s = posi[2] + self.waterDepth
        zeta = wavek * posi[0] - 2 * np.pi / self.wavePeriod * time
        yita = self.waveHeight / 2 * np.cos(zeta)

        if posi[2] < yita:
            horizonvelocity = piht * \
                              np.cosh(wavek * s) * np.cos(zeta) / np.sinh(wavek * self.waterDepth)
            vericalvelocity = piht * \
                              np.sinh(wavek * s) * np.sin(zeta) / np.sinh(wavek * self.waterDepth)
        else:
            horizonvelocity = 0.0
            vericalvelocity = 0.0
        velo = np.array([0.0, 0.0, 0.0])
        velo[0] = horizonvelocity
        velo[1] = 0.0
        velo[2] = vericalvelocity
        return velo

    def Get_Acce(self, posi, time):
        k = 2 * np.pi / self.waveLength
        piht = 2 * self.waveHeight * pow(pi / self.wavePeriod, 2)
        s = posi[2] + self.waterDepth
        zeta = k * posi[0] - 2 * np.pi / self.wavePeriod * time
        yita = self.waveHeight / 2 * np.cos(zeta)
        if posi[2] < yita:
            horizontalacceleration = piht * np.cosh(k * s) * np.sin(zeta) / np.sinh(k * self.waterDepth)
            vericalaccelateration = -piht * np.sinh(k * s) * np.cos(zeta) / np.sinh(k * self.waterDepth)
        else:
            horizontalacceleration = 0.0
            vericalaccelateration = 0.0
        acce = np.array([0.0, 0.0, 0.0])
        acce[0] = horizontalacceleration
        acce[1] = 0.0
        acce[2] = vericalaccelateration
        return acce

    def Get_Surface(self, area, time):
        wavek = 2 * np.pi / self.waveLength
        zeta = wavek * area[0] - 2 * np.pi / self.wavePeriod * time
        yita = self.waveHeight / 2 * np.cos(zeta)
        return yita

