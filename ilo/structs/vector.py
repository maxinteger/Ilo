# -*- coding: utf -*-

__author__="Vadasz Laszlo"
__date__ ="2009.10.26. 15:42:22"

import math
import numpy as np

"""
Ez a modul 4 féle vektor adatszerkezetet tartalmaz, egy általánost azaz
tetszőleges méretűt, és három specialiázáltat, 2, 3, és 4 dimenziósat.
"""


class Vector(np.ndarray, object):
    """
    Ez az osztály a C{numpy} C{ndarray} osztáláynak egy kiterjezstése,
    lényegében egy alias.

    @param  data:   A vektor adatai
    @type   data:   C{list}
    @param  type:   Az adatelemk típusa (alapéretlmezetten C{None} ebben az 
                    esetben autómatikusan állapítja meg a típust)
    @type   type:   C{numpy.dtype}
    @param  shape:  A vektor mérete (alapéretlmezetten C{None} ebben az esetben
                    Az adatok számával megegyező méretet vesz fel)
    """
    def __new__(cls, data, type=None, shape=None):
        data = np.array(data)
        if type == None: type = data.dtype
        if shape == None: shape = data.shape
        return np.ndarray.__new__(cls, shape  = shape,
                                       buffer = data,
                                       dtype  = type)

    @property
    def length(self):
        """A vektor hossza"""
        return math.sqrt((self ** 2).sum())

    @property
    def sqrLength(self):
        """A vektor hosszának négyzete"""
        return (self ** 2).sum()

    @property
    def normal(self):
        """A vektor normalizálása"""
        return self / self.length


class Vector2(Vector):
    """
    2D-s vektor

    Az általános C{Vector} specializálása, mely csak két elemű vektort képes
    csak elfogadni.
    Az adattagok névvel és indexxel is elérhetők
    """
    def __new__(cls, data, type = None):
        """
        2D vector inicilaizálása

        @param  data:   A vektor adatai
        @type   data:   C{list}
        @param  type:   Az adatelemk típusa (alapéretlmezetten C{None} ebben az
                        esetben autómatikusan állapítja meg a típust)
        @type   type:   C{numpy.dtype}
        """
        data = np.array(data)
        if type == None: type = data.dtype
        return Vector.__new__(cls, shape = (2,),
                                   data  = data,
                                   type  = type)

    @property
    def x (self):
        """A vetkor X azaz 1. értéke"""
        return self[0]

    @x.setter
    def x (self, value):
        self[0] = value

    @property
    def y (self):
        """A vetkor Y azaz 2. értéke"""
        return self[1]

    @x.setter
    def y (self, value):
        self[1] = value

    @staticmethod
    def zeros(type=None):
        """
        Üres, nulla elemekkel feltöltött 2D-s vektor létrehozása

        return: Nullákkal feltöltött 2D-s vektor
        rtype:  C{Vector2}
        """
        return Vector2([0.0,0.0], type)


class Vector3(Vector):
    """
    3D-s vektor

    Az általános C{Vector} specializálása, mely csak három elemű vektort képes
    csak elfogadni.
    Az adattagok névvel és indexxel is elérhetők
    """

    def __new__(cls, data, type = None):
        """
        3D vector inicilaizálása

        @param  data:   A vektor adatai
        @type   data:   C{list}
        @param  type:   Az adatelemk típusa (alapéretlmezetten C{None} ebben az
                        esetben autómatikusan állapítja meg a típust)
        @type   type:   C{numpy.dtype}
        """
        data = np.array(data)
        if type == None:
            type = data.dtype
        return Vector.__new__(cls, shape = (3,),
                                   data  = data,
                                   type  = type)
    @property
    def x (self):
        """A vetkor X azaz 1. értéke"""
        return self[0]

    @x.setter
    def x (self, value):
        self[0] = value

    @property
    def y (self):
        """A vetkor Y azaz 2. értéke"""
        return self[1]

    @y.setter
    def y (self, value):
        self[1] = value

    @property
    def z (self):
        """A vetkor Z azaz 3. értéke"""
        return self[2]

    @z.setter
    def z (self, value):
        self[2] = value

    @staticmethod
    def zeros(type=None):
        """
        Üres, nulla elemekkel feltöltött 3D-s vektor létrehozása

        return: Nullákkal feltöltött 3D-s vektor
        rtype:  C{Vector3}
        """
        return Vector3([0.0,0.0,0.0], type)



class Vector4(Vector):
    """
    4D-s vektor

    Az általános C{Vector} specializálása, mely csak négy elemű vektort képes
    csak elfogadni.
    Az adattagok névvel és indexxel is elérhetők
    """

    def __new__(cls, data, type = None):
        """
        4D vector inicilaizálása

        @param  data:   A vektor adatai
        @type   data:   C{list}
        @param  type:   Az adatelemk típusa (alapéretlmezetten C{None} ebben az
                        esetben autómatikusan állapítja meg a típust)
        @type   type:   C{numpy.dtype}
        """
        data = np.array(data)
        if type == None:
            type = data.dtype
        return Vector.__new__(cls, shape = (4,),
                                   data  = data,
                                   type  = type)

    @property
    def x (self):
        """A vetkor X azaz 1. értéke"""
        return self[0]

    @x.setter
    def x (self, value):
        self[0] = value

    @property
    def y (self):
        """A vetkor Y azaz 2. értéke"""
        return self[1]

    @y.setter
    def y (self, value):
        self[1] = value

    @property
    def z (self):
        """A vetkor Z azaz 3. értéke"""
        return self[2]

    @z.setter
    def z (self, value):
        self[2] = value

    @property
    def w (self):
        """A vetkor W azaz 4. értéke"""
        return self[3]

    @w.setter
    def w (self, value):
        self[3] = value

    @staticmethod
    def zeros(type=None):
        """
        Üres, nulla elemekkel feltöltött 4D-s vektor létrehozása

        return: Nullákkal feltöltött 4D-s vektor
        rtype:  C{Vector4}
        """
        return Vector4([0.0,0.0,0.0,0.0], type)
    
