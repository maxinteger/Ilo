# -*- coding: utf -*-

__author__="Vadasz Laszlo"
__date__ ="2009.10.01. 17:17:30"

from ilo.structs.vector import *
import numpy as np


"""
A grafikus megjelenítéshez elengedhetetlen alapvető
adatstuktúrákat tartalmaz modul
"""


class Vertex(object):
    """
    A csúcspontok koordinátáját és a hozzá tartozó normálvektort tartalmazza
    """

    __slots__ = ('index', 'vert', 'norm')

    def __init__(self, vertex, normal=None, index=None):
        """
        Vertex inicializálása

        @param  vertex:     A csúcspont koordinátái C{[x,y,z]} alakban
        @type   vertex:     C{list}
        @param  normal:     A normál vektor iránya C{[x,y,z]} alakban
        @type   normal:     C{list}
        @param  index:      Az objektum azonosítója
        @type   index:      C{int}
        """
        self.index  = index                                                     #:@ivar: A objektum azonosítója
        self.vert   = Vector3(vertex)                                           #:@ivar: Csúcspont koordinátái [x,y,z]
        self.norm   = None                                                      #:@ivar: A Normálvektor iránya [x,y,z]

        if normal != None: self.norm = Vector3 (normal)



################################################################################



class VertexUV(object):
    """
    Csúcsponthoz tartozó textúra koordináták
    """

    __slots__ = ('index', 'uv')

    def __init__(self, uv, index=None):
        """
        VertexUV inicilaizálása

        @param  uv:     2D-s textúra koordináta pár, U és V,  ahol M{U, V in [0,1]}
        @type   uv:     C{list}
        @param  index:  Az objektum azonosítója
        @type   index:  C{int}
        """
        self.index = index                                                      #:@ivar: A objektum azonosítója
        self.uv    = Vector2(uv)                                                #:@ivar: Koordináta pár (U, V)



################################################################################



class Edge(object):
    """
    Az él két csúcspontját és a hozzá akpcsolódó lapok azonosítóját tároló
    osztály
    """

    __slots__ = ('verts', 'faces')

    def __init__(self, v1, v2, f1, f2):
        """
        Edge inicializálása

        @param  v1:     Az él első csúcspontja
        @type   v1:     C{Vertex}
        @param  v2:     Az él második csúcspontja
        @type   v2:     C{Vertex}
        @param  f1:     Az első élhez kapcsolódó lap
        @type   f1:     C{Face}
        @param  f2:     Az második élhez kapcsolódó lap
        @type   f2:     C{Face}
        """
        self.verts    = [v1, v2]                                                #:@ivar: Az él csúcspontjai
        self.faces    = [f1, f2]                                                #:@ivar: Az élhez kapcsolódó lapok



################################################################################



class Face(object):
    """
    Lapok csúcspontjait, az azokhoz tartozó UV koordinátákat és a lap
    normálvektorát tároló osztály
    """

    __slots__ = ('index', 'verts', 'uvs', 'norm')

    def __init__(self, verteces, uvs, faceNormal=None, index=None):
        """
        Face inicilaizálása

        @param  verteces:   A lapot definiáló csúcspontok listája, [v1, v2, v3]
        @type   verteces:   C{list}
        @param  uvs:        A csúcspontokhoz tartozó textúra koordináta értékek
        @type   uvs:        C{list}
        @param  faceNormal: A lap normálvektora, C{None} esetén a csócspontokból
                            számítódik
        @param  index:      Az objektum azonosítója
        @type   index:      C{int}
        """
        self.index    = index                                                   #:@ivar: A objektum azonosítója
        self.verts    = verteces                                                #:@ivar: A laphoz tartozó csúcspontok
        self.uvs      = uvs                                                     #:@ivar: A csúcspontok textúra koordinátái
        self.norm     = faceNormal                                              #:@ivar: A lap normálvektora

        if self.norm == None:
            A, B, C   = verteces
            norm = Vector3(np.cross((B.vert - A.vert), (C.vert - A.vert)))
            self.norm =  norm.normal



################################################################################



class BoundBox():
    """
    Befoglaló doboz
    """

    __slots__ = ('__minPoint', '__maxpoint', 'minpoint', 'maxpoint')

    def __init__(self, data):
        """
        BoundBox inicializálása

        @param  data:   Vertex lista vagy (minPoint, maxPoint) tuple
        @type   data:   C{list} vagy C{tuple}
        """
        self.__minPoint = Vector3.zeros()                                       #:@ivar: A befoglaló kocka minimális csúcsa
        self.__maxPoint = Vector3.zeros()                                       #:@ivar: A befoglaló kocka maximális csúcsa

        if isinstance(data, list):
            def compar (x,y):
                if (x.vert > y.vert).any():
                    return 1
                elif (x.vert < y.vert).any():
                    return -1
                else:
                    return 0

            sortVert = sorted(data, compar)
            self.__minPoint = sortVert[0]
            self.__maxPoint = sortVert[-1]
        elif isinstance(data, tuple):
            self.__minPoint = data[0]
            self.__maxPoint = data[1]
        else:
            raise TypeError("Parameter is tuple (min, max) or list[vertex1, ...]")

    @property
    def minPoint(self):
        """A befoglaló doboz minimum pontja"""
        return self.__minPoint

    @property
    def maxPoint(self):
        """A befoglaló doboz maximum pontja"""
        return self.__maxPoint



################################################################################



class BoundShpere():
    """
    Befoglaló gömb
    """

    __slots__ = ('__center', '__radius', 'center', 'radius')

    def __init__(self, data):
        """
        BoundShpere inicializálása

        @param  data:   Vertex lista vagy (centerPoint, radius) tuple
        @type   data:   C{list} vagy C{tuple}
        """
        self.__center = Vector3.zeros()                                         #:@ivar: A bfeoglaló gömb középpontja
        self.__radius = 0                                                       #:@ivar: A befoglaló göm sugara

        if isinstance(data, list):
            center = Vector3([0,0,0])

            # average points to get approximate center
            for v in data:
                center += v.vert
            center /= len(data)

            # find maximum distance from center (sphere radius)
            maxDistance = -1.0
            for v in data:
                centerToVector = v.vert - center
                maxDistance = max(maxDistance, centerToVector.length)

            self.__center = center
            self.__radius = maxDistance
        elif isinstance(data, tuple):
            self.__center = data[0]
            self.__radius = data[1]
        else:
            raise TypeError("Parameter is tuple (center, radius) or list[vertex1, ...]")

    @property
    def center(self):
        """A befoglaló gömb középpontja"""
        return self.__center

    @property
    def radius(self):
        """A befoglaló gömb sugara"""
        return self.__radius