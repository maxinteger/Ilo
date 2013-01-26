# -*- coding: utf -*-

__author__="Vadasz Laszlo"
__date__ ="2010.04.08. 17:46:21"

import array

"""
Színkezeléssel kapcsoalatos függvényeket és osztáylokat tartalmazó modul
"""

class Color(object):
    """
    Színek kelezlésére szolgáló osztály, mely tartalmazza a három alapszínt
    (Red Green Blue) és az áttetszőségi értéket (Alpha)
    """

    __slots__ = ('__color',)

    def __init__(self, value):
        """
        Color inicializálása

        @param  value:  Szín komponenseket tartalmazó lista C{[R,G,B,a]} formában
        @type   value:  C{list}
        """
        self.__color = array.array("d",value)                                   #:@ivar: Szín komponenseket tároló lista

    @property
    def color(self):
        """Szín komponensek lista fromában"""
        return self.__color

    @color.setter
    def list(self, value):
        self.__color = array.array("d",value)

    @property
    def r (self):
        """Vörös szín összetevő értéke"""
        return self.__color[0]

    @r.setter
    def r (self, value):
        self.__color[0] = value

    @property
    def g (self):
        """Zöld szín összetevő értéke"""
        return self.__color[1]

    @g.setter
    def g (self, value):
        self.__color[1] = value

    @property
    def b (self):
        """Kék szín összetevő értéke"""
        return self.__color[2]

    @b.setter
    def b (self, value):
        self.__color[2] = value

    @property
    def a (self):
        """Áttetszőség szín összetevő értéke"""
        return self.__color[3]

    @a.setter
    def a (self, value):
        self.__color[3] = value