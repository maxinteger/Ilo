# -*- coding: utf -*-

__author__= ("Josh Beam", "Vadasz Laszlo")
__date__ ="2010.01.09. 7:45:11"

import math
import array
import numpy as np

from vector import *
from matrix import *

class Quanternion(object):
    """
    Speciális 4 dimenziós forgató vektor

    4 elemű vektor és a hozzátartozó műveletek.
    Segítségével számíthaó egy forgató mátrix

    Josh Beam - Drone/src/base/math.cpp~Quanternion osztály alapján
    http://joshbeam.com/software/drome_engine/
    """

    __slots__  = ('__quat',)

    def __init__(self):
        """
        Quanternion inicializálása
        """
        self.__quat = array.array("d",[0.0,0.0,0.0,0.0])                        #:@ivar: A quanternion értékeit tároló lista


    def clear(self):
        """
        Quanternion elemeinek nullázása
        """
        self.__quat = array.array("d",[0.0,0.0,0.0,0.0])
        return self


    def identity(self):
        """
        Quanternion egység vektor ahol a 4. elem 1 és a többi nulla
        """
        self.__quat = array.array("d",[0.0,0.0,0.0,1.0])
        return self


    def setFromAxis(self, axis, fi):
        """
        Adott tengelymenti elforgatás számítása

        return: Elforgatott Quanternion
        rtype:  C{Quanternion}
        """
        s = math.sin(fi/2)

        self.__quat[0] = axis[0] * s
        self.__quat[1] = axis[1] * s
        self.__quat[2] = axis[2] * s
        self.__quat[3] = math.cos(fi/2)

        return self


    def scale(self, f):
        """
        Quanternion skáláza
        """
        map( lambda x: x * f, self.__quat)


    def normalize(self):
        """
        Quanternion normalizálása
        """
        f = 1.0 / math.sqrt(np.dot(self.__quat, self.__quat) + self.w ** 2)
        self.scale(f)


    def conjugate(self):
        """
        Quanternion konjugáltja
        """
        self.__quat[0] = -self.__quat[0]
        self.__quat[1] = -self.__quat[1]
        self.__quat[2] = -self.__quat[2]


    def toMatrix(self):
        """
        Forgató mátrix számítása

        return: Forgató mátrix
        rtype:  C{Matrix4x4}
        """
        x, y, z, w = self.__quat

        x2 = 2 * x
        y2 = 2 * y
        z2 = 2 * z
        mat = [0]*16

        mat[0] = 1.0 - (y2 * y + z2 * z)
        mat[1] =        x2 * y + z2 * w
        mat[2] =        x2 * z - y2 * w
        mat[3] = 0.0

        mat[4] =        x2 * y - z2 * w
        mat[5] = 1.0 - (x2 * x + z2 * z)
        mat[6] =        y2 * z + x2 * w
        mat[7] = 0.0

        mat[8] =        x2 * z + y2 * w
        mat[9] =        y2 * z - x2 * w
        mat[10]= 1.0 - (x2 * x + y2 * y)
        mat[11]= 0.0

        mat[12]= 0.0
        mat[13]= 0.0
        mat[14]= 0.0
        mat[15]= 1.0

        return Matrix4x4(mat)


    def rotate(self, x, y, z):
        """
        Tengelyenkénti forgatás

        param   x:  Elforgatási szög az X tengely mentén fokban
        type    x:  C{float}
        param   y:  Elforgatási szög az Y tengely mentén fokban
        type    y:  C{float}
        param   z:  Elforgatási szög az Z tengely mentén fokban
        type    z:  C{float}
        """
        a_x = (1.0, 0.0, 0.0)
        a_y = (0.0, 1.0, 0.0)
        a_z = (0.0, 0.0, 1.0)

        q_x = Quanternion().setFromAxis(a_x, math.radians(x))
        q_y = Quanternion().setFromAxis(a_y, math.radians(y))
        q_z = Quanternion().setFromAxis(a_z, math.radians(z))

        self.__quat = ((q_x * q_y) * q_z).quat


    @property
    def quat(self):
        """A quanternion lista formájában"""
        return list(self.__quat)

    @quat.setter
    def quat(self, data):
        self.__quat = array.array("d", data)

    @property
    def x (self):
        """A quanternion X azaz 1. értéke"""
        return self.__quat[0]

    @x.setter
    def x (self, value):
        self.__quat[0] = value

    @property
    def y (self):
        """A quanternion Y azaz 2. értéke"""
        return self.__quat[1]

    @y.setter
    def y (self, value):
        self.__quat[1] = value

    @property
    def z (self):
        """A quanternion Z azaz 3. értéke"""
        return self.__quat[2]

    @z.setter
    def z (self, value):
        self.__quat[2] = value

    @property
    def w (self):
        """A quanternion W azaz 4. értéke"""
        return self.__quat[3]

    @w.setter
    def w (self, value):
        self.__quat[3] = value


    def __mul__(self, item):
        """
        Quanternion szorzás

        @param  item:   szorzó
        @type   item:   Quanternion
        """

        tmp = (self.w * item.w) - np.dot(self.quat[:3], item.quat[:3])

        v1 = Vector3(np.cross(self.quat[:3], item.quat[:3]))
        v2 = Vector3(self.quat[:3]) * item.w
        v3 = Vector3(item.quat[:3]) * self.w

        v1 = (v1 + v2) + v3

        self.quat = (list(v1) + [tmp])

        return self
