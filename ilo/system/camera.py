# -*- coding: utf -*-

__author__="Vadasz Laszlo"
__date__ ="2010.01.09. 7:36:41"

import math
from ilo.system.gfx import *
from ilo.structs.vector import *
from ilo.structs.matrix import *
from ilo.structs.quanternion import *


"""Kamera modul"""

class Camera(object):
    """
    A kemera vezérlését és az ehhez kapcsolódó számításokat végző osztály
    """

    __slots__ = ('__q','__matrix', '__position', '__rx', '__ry', '__rz', '__frustum')

    def __init__(self):
        """
        Camera inicializálása
        """
        self.__q            = Quanternion()                                     #:@ivar: A forgatási számításokat végző objetum
        self.__matrix       = Matrix4x4.identity()                              #:@ivar: Aktuális transzformációs mátrix
        self.__position     = Vector3.zeros()                                   #:@ivar: A kamera poziciója
        self.__rx           = 0.0                                               #:@ivar: Forgatás az X tengely körül - Pitch
        self.__ry           = 0.0                                               #:@ivar: Forgatás az Y tengely körül - roll
        self.__rz           = 0.0                                               #:@ivar: Forgatás az Z tengely körül - yaw
        self.__frustum      = []                                                #:@ivar: Látomezőt határoló síkok

    def clear(self):
        """
        Alapértelmezett értékek visszalállítása
        """
        self.__position = Vector3.zeros()

        self.__rx = 0.0     # pitch
        self.__ry = 0.0     # roll
        self.__rz = 0.0     # yaw

        self.update()


    def moveTo(self, x, y, z):
        """
        Kamera mozgatása a három koordináta szerint

        @param  x:  Kamera mozgatása az x tengely mentén
        @type   x:  C{float}
        @param  y:  Kamera mozgatása az y tengely mentén
        @type   y:  C{float}
        @param  z:  Kamera mozgatása az z tengely mentén
        @type   z:  C{float}
        """
        self.__position.x += x
        self.__position.y += y
        self.__position.z += z


    def flyTo(self, speed):
        """
        Replülés azaz a kamera az aktuális irányba halad

        @param  speed:  A haladás sebessége, negatív is lehet
        @type   speed:  C{float}
        """
        self.__position.x += math.sin(math.radians(-self.__rz)) * speed
        self.__position.y += math.cos(math.radians(-self.__rz)) * speed


    def update(self):
        """
        A transformációs mátrix aktualizálása a kamera adatai alapján
        """
        # X rotation
        r_mat = Matrix4x4.homRotationX(self.__rx)
        t_mat = Matrix4x4.identity()

        t_mat[0, 3] = -self.__position.x #+ self.__translate.x
        t_mat[1, 3] = -self.__position.y #+ self.__translate.y
        t_mat[2, 3] = -self.__position.z #+ self.__translate.z

        self.__q.rotate(90.0, self.__rz, self.__ry)
        self.__matrix = self.__q.toMatrix()
#        t_mat[0, 3] -= self.__matrix[2, 0] * self.kick
#        t_mat[1, 3] -= self.__matrix[2, 1] * self.kick
#        t_mat[2, 3] -= self.__matrix[2, 2] * self.kick

        self.__matrix = (r_mat * (self.__matrix *  t_mat))



    def updateFrustum(self):
        """
        A látómezőt határoló síkok számítása aktualizálása
        """
        # @type gfx GLContext
        gfx = GLContext.getInstance()
        
        product     = gfx.matrix.getMatrix(Gfx.MODELVIEW)
        projection  = gfx.matrix.getMatrix(Gfx.PROJECTION)
        product     *= projection
        productV    = Vector3([product[0][3] - product[0][0],
                               product[1][3] - product[1][0],
                               product[2][3] - product[2][0]])

        productD= product[3][3] - product[3][0]
        
        def calc (item):
            item.vec    = productV
            item.d      = productD
            scale       = 1.0 / (np.dot(item.vec, item.vec))
            item.vec    *= scale
            item.d      *= scale

        map(calc, self.__frustum)


    def pointInFrustum(self, v):
        """
        A megadott pont a látómezőben van vagy sem?

        @param  v:  Egy pont a térben melyről tudni szeretnénk, hogy a látó, mezőben van-e?
        @type   v:  C{Vector3}

        @return:    C{True} ha C{v} pont a látómezőben van, különben C{False}
        @rtype:     C{bool}
        """
        dir = Vector3()
        dir.x = self.__matrix[2][0]
        dir.y = self.__matrix[2][1]
        dir.z = self.__matrix[2][2]

        tmp = self.__position - v

        if (np.dot(dir, tmp) >= 0.0):
            return False

        return True


    def sphereInFrustum(self, point, radius):
        """
        A megadott gömb a látómező része-e?

        @param  point:  A gömb középpontja
        @type   point:  C{Vector3}
        @param  radius: A gömb sugara
        @type   radius: C{float}
        """
        for item in self.__frustum:
            if item.TestPoint(point) < -radius:
                return False
        return True


    @property
    def matrix(self):
        """Az aktuális transzformációs mátrix"""
        return self.__matrix

    @property
    def position(self):
        """A kamera aktuális pozíciója"""
        return self.__position

    @property
    def rotateX(self):
        """X tengely körüli elforgatás"""
        return self.__rx

    @rotateX.setter
    def rotateX(self, fi):
        self.__rx += fi
        if (self.__rx > 90.0):
            self.__rx = 90.0
        elif (self.__rx < -90.0):
            self.__rx = -90.0

    @property
    def rotateY(self):
        """Y tengely körüli elforgatás"""
        return self.__ry

    @rotateY.setter
    def rotateY(self, fi):
        self.__ry += fi

    @property
    def rotateZ(self):
        """Z tengely körüli elforgatás"""
        return self.__rz

    @rotateZ.setter
    def rotateZ(self, fi):
        self.__rz += fi
