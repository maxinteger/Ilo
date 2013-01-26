# -*- coding: utf -*-

__author__="Vadasz Laszlo"
__date__ ="2009.10.26. 16:20:31"

import math
import numpy as np

"""
Mátrix megvalósítások melyek mind a C{numpy} modulra épülnek.
Az itt található osztályok a C{numpy}  C{ndarray} osztályából származnak és egy
speciális esetet valósítanak meg.

A főbb eltérések a méretben nyílvánulnak meg:
 - általános mátrix
 - 2x2-es mátrix
 - 3x3-es mátrix
 - 4x4-es mátrix

Továbbá a 3D-s grafikában gyakran használt műveletekre különön statkus metódok
vannak definiálva

@see U{numpy <http://numpy.org>}
"""

class Matrix(np.ndarray):
    """
    Általános mátrix.
    Mérete tetszőlegesen beállítható
    """
    def __new__(cls, data, type = None):
        data = np.matrix(data)
        if type == None:
            type = data.dtype
        return np.ndarray.__new__(cls, shape  =data.shape,
                                       buffer =data,
                                       dtype  =type)


class Matrix2x2(np.ndarray):
    """
    2x2-es mátrix
    """
    def __new__(cls, data, type = None):
        data = np.matrix(data)
        if type == None:
            type = data.dtype
        return np.ndarray.__new__(cls, shape  =(2,2),
                                       buffer =data,
                                       dtype  =type)

    def __init__(self, data, dtype=None, copy=False):
        """
        2x2-es mátrix inicilizálása

        @param  data:   Mátrix értékei
        @type   data:   C{List}
        @param  type:   Mátrix értékeinek típusa
        @type   type:   C{String}
        """
        pass

    @staticmethod
    def zeros(type=None):
        """
        Nulla értékekkel feltöltött 2x2-es mátrix

        @param  type:   Mátrix értékeinek típusa
        @type   type:   C{String}

        @return: 2x2-es nulla mátrix
        @rtype:  C{Matrix2x2}
        """
        return Matrix2x2(np.zeros((2,2)))

    @staticmethod
    def identity(self, type=None):
        """
        2x2-es egységmátrix ahol minden elem nulla kivéve a főátlóban lővőket
        mert ott egyesek vannak.

        @param  type:   Mátrix értékeinek típusa
        @type   type:   C{String}

        @return: 2x2-es egységmátrix
        @rtype:  C{Matrix2x2}
        """
        return Matrix2x2([[1.0, 0.0],
                          [0.0, 1.0]], type)

    @staticmethod
    def rotation(angle):
        """
        2x2-es forgatómátrix

        @param  angle:  forgatás szöge radiánban
        @type   angle:  C{float}

        @return: 2x2-es forgató mátrix
        @rtype:  C{Matrix2x2}
        """
        c = math.cos(angle)
        s = math.sin(angle)
        return Matrix2x2([[c, -s],
                          [s, c]])



class Matrix3x3(np.matrix):
    """
    3x3-as mátrix
    """

    def __new__(cls, data, type = None):
        data = np.matrix(data)
        if type == None:
            type = data.dtype
        return np.ndarray.__new__(cls, shape  =(3,3),
                                       buffer =data,
                                       dtype  =type)

    def __init__(self, data, dtype=None, copy=False):
        """
        3x3-as mátrix inicilizálása

        @param  data:   Mátrix értékei
        @type   data:   C{List}
        @param  type:   Mátrix értékeinek típusa
        @type   type:   C{String}
        """
        pass

    @staticmethod
    def zeros(type=None):
        """
        Nulla értékekkel feltöltött 3x3-es mátrix

        @param  type:   Mátrix értékeinek típusa
        @type   type:   C{String}

        @return: 3x3-as nulla mátrix
        @rtype:  C{Matrix3x3}
        """
        return Matrix3x3(np.zeros((3,3)), type)

    @staticmethod
    def identity(type=None):
        """
        3x3-as egységmátrix ahol minden elem nulla kivéve a főátlóban lővőket
        mert ott egyesek vannak.

        @param  type:   Mátrix értékeinek típusa
        @type   type:   C{String}

        @return: 3x3-as egységmátrix
        @rtype:  C{Matrix3x3}
        """
        return Matrix2x2([[1.0, 0.0, 0.0],
                          [0.0, 1.0, 0.0],
                          [0.0, 0.0, 1.0]], type)

    @staticmethod
    def rotationX(angle):
        """
        3x3-as forgatómátrix amely az X tengely mentén végez forgatási
        transzformációt

        @param  angle:  forgatás szöge radiánban
        @type   angle:  C{float}

        @return: 3x3-as X tengely menti forgató mátrix
        @rtype:  C{Matrix3x3}
        """
        angle = math.radians(angle)
        c = math.cos(angle)
        s = math.sin(angle)
        return Matrix3x3([[1.0, 0.0 , 0.0 ],
                          [0.0, c   , -s  ],
                          [0.0, s   ,  c  ]])

    @staticmethod
    def rotationY(angle):
        """
        3x3-as forgatómátrix amely az Y tengely mentén végez forgatási
        transzformációt

        @param  angle:  forgatás szöge radiánban
        @type   angle:  C{float}

        @return: 3x3-as Y tengely menti forgató mátrix
        @rtype:  C{Matrix3x3}
        """
        angle = math.radians(angle)
        c = math.cos(angle)
        s = math.sin(angle)
        return Matrix3x3([[c  , 0.0, s  ],
                          [0.0, 1.0, 0.0],
                          [-s , 0.0, c  ]])

    @staticmethod
    def rotationZ(angle):
        """
        3x3-as forgatómátrix amely az Z tengely mentén végez forgatási
        transzformációt

        @param  angle:  forgatás szöge radiánban
        @type   angle:  C{float}

        @return: 3x3-as Z tengely menti forgató mátrix
        @rtype:  C{Matrix3x3}
        """
        angle = math.radians(angle)
        c = math.cos(angle)
        s = math.sin(angle)
        return Matrix3x3([[c  , -s  , 0.0],
                          [s  ,  c  , 0.0],
                          [0.0,  0.0, 1.0]])


class Matrix4x4(np.matrix):
    """
    4x4-es mátrix
    """
    def __new__(cls, data, type = None):
        data = np.matrix(data)
        if type == None:
            type = data.dtype
        return np.ndarray.__new__(cls, shape  =(4,4),
                                       buffer =data,
                                       dtype  =type)

    def __init__(self, data, dtype=None, copy=False):
        """
        4x4-es mátrix inicilizálása

        @param  data:   Mátrix értékei
        @type   data:   C{List}
        @param  type:   Mátrix értékeinek típusa
        @type   type:   C{String}
        """
        pass

    @staticmethod
    def zeros(type=None):
        """
        Nulla értékekkel feltöltött 4x4-es mátrix

        @param  type:   Mátrix értékeinek típusa
        @type   type:   C{String}

        @return: 4x4-es nulla mátrix
        @rtype:  C{Matrix4x4}
        """
        return Matrix4x4(np.zeros((4,4)), type)

    @staticmethod
    def identity(type=None):
        """
        4x4-es egységmátrix ahol minden elem nulla kivéve a főátlóban lővőket
        mert ott egyesek vannak.

        @param  type:   Mátrix értékeinek típusa
        @type   type:   C{String}

        @return: 4x4-es egységmátrix
        @rtype:  C{Matrix4x4}
        """
        return Matrix4x4([[1.0, 0.0, 0.0, 0.0],
                          [0.0, 1.0, 0.0, 0.0],
                          [0.0, 0.0, 1.0, 0.0],
                          [0.0, 0.0, 0.0, 1.0]], type)

    @staticmethod
    def homRotationX(angle):
        """
        4x4-as forgatómátrix amely a 3x3-as mátrixhoz hasonlóan az X tengely
        mentén végez forgatási transzformációt, de ebben az esetben homogén
        koordinátarendszerben

        @param  angle:  forgatás szöge radiánban
        @type   angle:  C{float}

        @return: 4x4-as X tengely menti homogén koordinátás forgató mátrix
        @rtype:  C{Matrix4x4}
        """
        angle = math.radians(angle)
        c = math.cos(angle)
        s = math.sin(angle)
        return Matrix4x4([[1.0, 0.0, 0.0, 0.0],
                          [0.0, c  , -s , 0.0],
                          [0.0, s  ,  c , 0.0],
                          [0.0, 0.0, 0.0, 1.0]])

    @staticmethod
    def homRotationY(angle):
        """
        4x4-as forgatómátrix amely a 3x3-as mátrixhoz hasonlóan az Y tengely
        mentén végez forgatási transzformációt, de ebben az esetben homogén
        koordinátarendszerben

        @param  angle:  forgatás szöge radiánban
        @type   angle:  C{float}

        @return: 4x4-as Y tengely menti homogén koordinátás forgató mátrix
        @rtype:  C{Matrix4x4}
        """
        angle = math.radians(angle)
        c = math.cos(angle)
        s = math.sin(angle)
        return Matrix4x4([[c  , 0.0, s  , 0.0],
                          [0.0, 1.0, 0.0, 0.0],
                          [-s , 0.0, c  , 0.0],
                          [0.0, 0.0, 0.0, 1.0]])

    @staticmethod
    def homRotationZ(angle):
        """
        4x4-as forgatómátrix amely a 3x3-as mátrixhoz hasonlóan az Z tengely
        mentén végez forgatási transzformációt, de ebben az esetben homogén
        koordinátarendszerben

        @param  angle:  forgatás szöge radiánban
        @type   angle:  C{float}

        @return: 4x4-as Z tengely menti homogén koordinátás forgató mátrix
        @rtype:  C{Matrix4x4}
        """
        angle = math.radians(angle)
        c = math.cos(angle)
        s = math.sin(angle)
        return Matrix4x4([[c  ,  -s, 0.0, 0.0],
                          [s  ,   c, 0.0, 0.0],
                          [0.0, 0.0, 1.0, 0.0],
                          [0.0, 0.0, 0.0, 1.0]])