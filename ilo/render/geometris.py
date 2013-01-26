# -*- coding: utf -*-

__author__="Vadasz Laszlo"
__date__="2009.08.27. 13:09:08"


from ilo.system.camera import *
import math

from OpenGL.GL import *
from OpenGL.raw.GL.VERSION.GL_3_0 import *

from ilo.config import *
from ilo.filereader.model.ase import loadASEFile
from ilo.messages.exceptios import IloError
from ilo.structs.d3d import *
from ilo.structs.vector import *
from ilo.structs.matrix import *

class ModelGeometryLibraly(object):
    """
    Geometriatár
    Kétszintű tárrendeszer, melyben egyedi geometria adatok vannak eltárolva
    A geometria adatok geometria könyvtárakba vannak rendezve.
    Ez az ossztály a tárrednszer kezelését végzi.
    """

    def __init__(self):
        """
        Geometriatár inicilaizálása
        """
        self.__geometrylLibs = {}

    
    def addGeometryLibraly(self, geomLib):
        """
        Új geometria könyvtár hozzáadása a geometriatárhoz

        gaomLib = Az új geometria könyvtár azonosítója
        """
        if name not in self.__geometrylLibs:
            self.__geometrylLibs[geomLib] = {}
        else:
            raise IloError ("A megadott geometriakönytár már létezik: " + geomLib)


    def addGeometry(self, geomLib, id, geom):
        """
        Új geometria hozzáadása egy létező geometria könyvtárhoz

        geomLib = A beolvasott objektumok geometria könyvtára
        id      = Az új geometria azonosítója
        geom    = Az új geometria
        """
        if geomLib not in self.__geometrylLibs:
            self.addGeometryLibraly(geomLib)

        if id not in self.__geometrylLibs[geomLib]:
            geom.glInit__()
            self.__geometrylLibs[geomLib][id] = geom
        else:
            raise IloError ("A '" + id + "' geometria azonosító már létezik a '\
                            " + geomLib + "' geometria könyvtárban")

        return self.__geometrylLibs[geomLib][id]


    def addGeometryFromFile(self, geomLib, fileName, geomIDs = None, format = "ase"):
        """
        Geometriák beolvasása (ASE) fájlból
        Egy geometria fájl több objektumot is tárolhat. A metódus a `geomIDs`-
        ban felsorol azonosítók alapján olvassa be az objektumokat, ha ez nincs
        meg adva akkor az összes objektumot beolvassa a megadott geometria
        könyvtárba. Minden objektum a fájlban található objetumazonosítóval
        érhető el.

        geomLib     = A beolvasott objektumok geometria könyvtára
        fileName    = A beolvasandó fájl elrési útvonala
        geomIDs     = Lista mely a beolvasandó objektumok azonosítóját
                      tartalmazza, None érték esetén minden objektumot beolvas
        format      = A forrás fájl formátuma
        """
        if format == "ase":
            geoms = loadASEFile(fileName)
        else:
            raise IloError("Ismeretlen fájlformátum!" + format)

        for geom in geoms:
            if geomIDs  == None or geom.name in geomIDs:
                self.addGeometry(geomLib, geom.name, Geometry(geom))


    def hasGeometryLibraly(self, geomLib):
        """Létezik-e a megadott geometria könyvtár"""
        return geomLib in self.__geometrylLibs


    def hasGeometry(self, geomLib, geomID):
        """Létezik-e a megdott geometria a adott geometria könyvtárban"""
        if geomLib in self.__geometrylLibs:
            return geomID in self.__geometrylLibs[geomLib]
        return False


    def hasGeometryById(self, geomLibID):
        """Létezik-e a megdott geometria a adott geometria könyvtárban"""
        return self.hasGeometry(*geomLibID.split("."))


    def getGeometry(self, geomLib, geomID):
        """Geometria lekérése a geometriatárból"""
        return self.__geometrylLibs[geomLib][geomID]


    def getGeometryById(self, geomLibID):
        """Geometria lekérése a geometriatárból"""
        return self.getGeometry(*geomLibID.split("."))


    def getAllGeometry(self, geomLib):
        """Az összes geometria lekérése a megadott geometria könyvtából"""
        return self.__geometrylLibs[geomLib]


    def removeGeometryLibraly(self, geomLib):
        """A megadott geometria könyvár törlése az össze elemével együtt"""
        if geomLib in self.__geometrylLibs:
            del self.__geometrylLibs[id]


    def removeGeometry(self, geomLib, geomID):
        """Geometria törlése a megadott geometria könyvtárból"""
        del self.__geometrylLibs[geomLib][geomID]


    def removeGeometryById(self, geomLibID):
        """Geometria törlése a megadott geometria könyvtárból"""
        self.getGeometry(*geomLibID.split("."))


    def removeAllGeometry(self):
        """Minden geometria és geometria könyvtár törlése a geometria tárból"""
        for lib in self.__geometrylLibs:
            for geom in lib:
                geom.remove()
        del self.__geometrylLibs
        self.__geometrylLibs = {}




class WirePrimitivGeometry(object):
    WIRE_CROSS          = "wCross"
    WIRE_AXIS           = "wAxis"
    WIRE_PLANE          = "wPlane"
    WIRE_GRID           = "wGrid"
    WIRE_CUBE           = "wCube"
    WIRE_CIRCLE         = "wCircle"
    WIRE_CYLINDER       = "wCylinder"
    WIRE_SPHERE         = "wSphere"
    WIRE_TRIANGLE_CONE  = "wTCone"
    WIRE_QUAD_CONE      = "wQCone"
    WIRE_CIRCLE_CONE    = "wCCone"


    def __init__(self, type, params):

        self.__objectList = {
            WirePrimitivGeometry.WIRE_CROSS:           self.__genWCross,
            WirePrimitivGeometry.WIRE_AXIS:            self.__genWAxis,
            WirePrimitivGeometry.WIRE_PLANE:           self.__genWPlane,
            WirePrimitivGeometry.WIRE_GRID:            self.__genWGrid,
            WirePrimitivGeometry.WIRE_CUBE:            self.__genWCube,
            WirePrimitivGeometry.WIRE_CIRCLE:          self.__genWCircle,
            WirePrimitivGeometry.WIRE_CYLINDER:        self.__genWCylinder,
            WirePrimitivGeometry.WIRE_SPHERE:          self.__genWSphere,
            WirePrimitivGeometry.WIRE_TRIANGLE_CONE:   self.__genWTCone,
            WirePrimitivGeometry.WIRE_QUAD_CONE:       self.__genWQCone,
            WirePrimitivGeometry.WIRE_CIRCLE_CONE:     self.__genWCCone
        }

        self.type = type
        self.params = params
        self.__glList = None

    def glInit__(self):
        self.__glList = glGenLists(1)
        glNewList(self.__glList, GL_COMPILE)

        self.__objectList[self.type](*self.params)

        glEndList()

        del self.__objectList, self.params

    def render(self):
        if self.__glList:
            glCallList(self.__glList)

    def __genWAxis(self, size):
        glLineWidth (5.0)
        glBegin(GL_LINES)
        #axis X
        glColor3f(0.0, 0.0, 1.0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(size, 0.0, 0.0)
        #axis Y
        glColor3f(0.0, 1.0, 0.0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0.0, size, 0.0)
        #axis Z
        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0.0, 0.0, size)
        glEnd()


    def __genWCross(self):
        glBegin(GL_LINES)
        glVertex3f(-0.5, 0.0, 0.0)
        glVertex3f(0.5, 0.0, 0.0)
        glVertex3f(0.0, -0.5, 0.0)
        glVertex3f(0.0, 0.5, 0.0)
        glVertex3f(0.0, 0.0, -0.5)
        glVertex3f(0.0, 0.0, 0.5)
        glEnd()

    def __genWPlane(self, w = 1, h = 1):
        w2 = w / 2
        h2 = h / 2
        glBegin(GL_LINE_LOOP)
        glVertex3f(-w2, -h2, 0.0)
        glVertex3f(w2, -h2, 0.0)
        glVertex3f(w2, h2, 0.0)
        glVertex3f(-w2, h2, 0.0)
        glEnd()

    def __genWGrid(self, paces = 10, space = 20):
        half = paces / 2
        glBegin(GL_LINES)
        for i in xrange(-half, half + 1):
            glVertex3f(half * space, i * space, 0.0)
            glVertex3f(-half * space, i * space, 0.0)
            glVertex3f(i * space, half * space, 0.0)
            glVertex3f(i * space, -half * space, 0.0)
        glEnd()

    def __genWCube(self, w = 1, h = 1, d = 1):
        w2 = w / 2
        h2 = h / 2
        d2 = d / 2
        glBegin(GL_LINES)
        glVertex3f(-w2, -h2, -d2)
        glVertex3f(-w2, -h2, d2)
        glVertex3f(w2, -h2, -d2)
        glVertex3f(w2, -h2, d2)
        glVertex3f(w2, h2, -d2)
        glVertex3f(w2, h2, d2)
        glVertex3f(-w2, h2, -d2)
        glVertex3f(-w2, h2, d2)
        glEnd()
        glTranslate(0.0, 0.0, -d2)
        self.__genWPlane(w, h)
        glTranslate(0.0, 0.0, d-d2)
        self.__genWPlane(w, h)

    def __genWCircle(self, r, segments = 16):
        segmentAngle = (math.pi * 2) / segments
        glBegin(GL_LINE_LOOP)
        for i in xrange(segments):
            glVertex3f(math.cos(i * segmentAngle) * r, math.sin(i * segmentAngle) * r, 0)
        glEnd()

    def __genWCylinder(self, r, h, segments = 16):
        segmentAngle = (math.pi * 2) / segments
        h2 = h / 2
        glBegin(GL_LINES)
        for i in xrange(segments):
            glVertex3f(math.cos(i * segmentAngle) * r, math.sin(i * segmentAngle) * r, h2)
            glVertex3f(math.cos(i * segmentAngle) * r, math.sin(i * segmentAngle) * r, -h2)
        glEnd()
        glTranslate(0.0, 0.0, -h2)
        self.__genWCircle(r, segments)
        glTranslate(0.0, 0.0, h-h2)
        self.__genWCircle(r, segments)

    def __genWSphere(self, r, segments = 16):
        self.__genWCircle(r, segments)
        glRotate(90.0, 1, 0, 0)
        self.__genWCircle(r, segments)
        glRotate(90.0, 0, 1, 0)
        self.__genWCircle(r, segments)

    def __genWTCone(self):
        pass

    def __genWQCone(self):
        pass

    def __genWCCone(self):
        pass

