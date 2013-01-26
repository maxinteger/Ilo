# -*- coding: utf -*-

__author__="Vadasz Laszlo"
__date__ = "2009.07.24. 16:28:55"

from OpenGL.GL import *
from ilo.render.display import RenderObject
from ilo.libralis.geometris import WirePrimitivGeometry
from ilo.messages.events import Event

#TODO instrukció a helperekhez
#print "A segéd objektumok (helpers) megjelenítése nincs optimalizálva, ezért..."


class BaseHelper(RenderObject):
    def __init__(self, name, geometry):
        RenderObject.__init__(self, name, geometry)

        self.geometry.glInit__()

        self.color = [1.0, 1.0, 0.0]

#        del self.material
#        del self.blendMode
    def render__(self, shadowRenderMode, target = None):
        glPushMatrix()
        glPushAttrib(GL_ALL_ATTRIB_BITS)
        glDisable(GL_LIGHTING)
        glTranslate(*self.coord)
        glRotate(self.angle[0],1.0, 0.0, 0.0)
        glRotate(self.angle[1],0.0, 1.0, 0.0)
        glRotate(self.angle[2],0.0, 0.0, 1.0)
        glScale(*self.scale)
        if self.visible and self.geometry != None:
            if not shadowRenderMode:
                glColor3fv(self.color)
                self.geometry.render()
                
            if self.hasEventListener(Event.RENDERED):
                self.dispatchEvent(Event(Event.RENDERED))
        glPopAttrib()
        glPopMatrix()

    @property
    def showNormals(self):
        print "A segéd objektumok vertex normálvektora nen megjeleníthető!"
        return False

    @showNormals.setter
    def showNormals(self, value):
        print "A segéd objektumok vertex normálvektora nen megjeleníthető!"


class AxisHelper(BaseHelper):
    def __init__(self, size):
        BaseHelper.__init__(self,
                            "CrossHelper",
                            WirePrimitivGeometry(WirePrimitivGeometry.WIRE_AXIS,
                                                 [size]))

class CrossHelper(BaseHelper):
    def __init__(self):
        BaseHelper.__init__(self,
                            "CrossHelper",
                            WirePrimitivGeometry(WirePrimitivGeometry.WIRE_CROSS,
                                                 []))

class PlaneHelper(BaseHelper):
    def __init__(self, width = 1, heigth = 1):
        BaseHelper.__init__(self,
                            "PlaneHelper",
                            WirePrimitivGeometry(WirePrimitivGeometry.WIRE_PLANE,
                                                 [width, heigth]))

class GridHelper(BaseHelper):
    def __init__(self, paces = 1, space= 1):
        BaseHelper.__init__(self,
                            "PlaneHelper",
                            WirePrimitivGeometry(WirePrimitivGeometry.WIRE_GRID,
                                                 [paces, space]))

class CubeHelper(BaseHelper):
    def __init__(self, width = 1, heigth = 1, depth = 1):
        BaseHelper.__init__(self,
                            "CubeHelper",
                            WirePrimitivGeometry(WirePrimitivGeometry.WIRE_CUBE,
                                                 [width, heigth, depth]))

class CircleHelper(BaseHelper):
    def __init__(self, radius = 1):
        BaseHelper.__init__(self,
                            "CirclesHelper",
                            WirePrimitivGeometry(WirePrimitivGeometry.WIRE_CIRCLE,
                                                 [radius]))

class CylinderHelper(BaseHelper):
    def __init__(self, radius = 1, heigth = 1):
        BaseHelper.__init__(self,
                            "CylinderHelper",
                            WirePrimitivGeometry(WirePrimitivGeometry.WIRE_CYLINDER,
                                                 [radius, heigth]))

class SphereHelper(BaseHelper):
    def __init__(self, radius = 1):
        BaseHelper.__init__(self,
                            "PlaneHelper",
                            WirePrimitivGeometry(WirePrimitivGeometry.WIRE_SPHERE,
                                                 [radius]))
