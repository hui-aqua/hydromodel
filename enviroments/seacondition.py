# writer: hui.cheng@uis.no
# please contact the writer if there is any questions
# in this library, I assume the wave is coming from -X, and long X-axis,
# Z is the gravity direction,Z=0 is the water level, and the water is below z=0
# reference
import numpy as np
from numpy import pi


class IdeLinwave:
    """
    Using idealized linear waves theory      \n
    To define this class, need to import:    \n
    waveheight [m], wavelength [m], waveperiod [s], waterdepth [m] \n
    in this library, I assume the wave is coming from -X, and long X-axis,
    Z is the gravity direction,Z=0 iz the water level, and the water is below z=0
    If there are any questions, please contact hui.cheng@uis.no
    """

    def __init__(self, waveHeight=1.0, waveLength=25.0, waterDepth=60.0):
        self.waveHeight = waveHeight
        self.waveLength = waveLength
        self.wavePeriod = np.sqrt(2 * pi * waveLength / 9.81)
        self.waterDepth = waterDepth
        self.wavek = 2 * np.pi / self.waveLength
        self.piht = np.pi * self.waveHeight / self.wavePeriod
        self.piht2 = 2 * self.waveHeight * pow(pi / self.wavePeriod, 2)

    def __str__(self):
        s0 = 'The environment is idealized linear wave condition and the specific parameters are:\n'
        s1 = 'water Depth= ' + str(self.waterDepth) + ' m\n'
        s2 = 'wave Period= ' + str(self.wavePeriod) + ' s\n'
        s3 = 'wave Length= ' + str(self.waveLength) + ' m\n'
        s4 = 'wave Height= ' + str(self.waveHeight) + ' m\n'
        S = s0 + s1 + s2 + s3 + s4
        return S

    def Get_Velo(self, posi, time):
        s = posi[2] + self.waterDepth
        zeta = self.wavek * posi[0] - 2 * np.pi / self.wavePeriod * time
        yita = self.Get_Surface(posi, time)
        if posi[2] < yita:
            horizonvelocity = self.piht * np.cosh(self.wavek * s) * np.cos(zeta) / np.sinh(self.wavek * self.waterDepth)
            vericalvelocity = self.piht * np.sinh(self.wavek * s) * np.sin(zeta) / np.sinh(self.wavek * self.waterDepth)
        else:
            horizonvelocity = 0.0
            vericalvelocity = 0.0
        velo = np.array([0.0, 0.0, 0.0])
        velo[0] = horizonvelocity
        velo[1] = 0.0
        velo[2] = vericalvelocity
        return velo

    def Get_Acce(self, posi, time):
        s = posi[2] + self.waterDepth
        zeta = self.wavek * posi[0] - 2 * np.pi / self.wavePeriod * time
        yita = self.waveHeight / 2 * np.cos(zeta)
        if posi[2] < yita:
            horizontalacceleration = self.piht2 * np.cosh(self.wavek * s) * np.sin(zeta) / np.sinh(
                self.wavek * self.waterDepth)
            vericalaccelateration = -self.piht2 * np.sinh(self.wavek * s) * np.cos(zeta) / np.sinh(
                self.wavek * self.waterDepth)
        else:
            horizontalacceleration = 0.0
            vericalaccelateration = 0.0
        acce = np.array([0.0, 0.0, 0.0])
        acce[0] = horizontalacceleration
        acce[1] = 0.0
        acce[2] = vericalaccelateration
        return acce

    def Get_Surface(self, posi, time):
        zeta = self.wavek * posi[0] - 2 * np.pi / self.wavePeriod * time
        yita = self.waveHeight / 2 * np.cos(zeta)
        return yita
