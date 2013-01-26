# -*- coding: utf -*-

__author__="Vadasz Laszlo"
__date__ = "2009.09.01. 14:57:06"
__all__ = ["LightLibraly"]

from OpenGL.GL import *
from ilo.messages.exceptios import IloError
from ilo.render.display import RenderObject
from ilo.structs.vector import Vector3

"""
Ebben a modulban a fényforrással kapcsolatos osztályok helyzekednek el.
"""

class LightLibraly(object):
    """
    Ez az osztály végzi a fényforrások regisztrálását.
    Maximum a rendszer által támogatott mennyiségű fényforrás igényelhető.
    """

    __slots__  = ('__maxLights', '__lightSet', '__linkedLights', '__lighting', '__scene')

    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        @raise SingletonClassError: Az osztály csak egyszer példányosítható
        """
        if not cls._instance:
            cls._instance = super(LightLibraly, cls).__new__(cls)
            return cls._instance
        else:
            raise SingletonClassError("Csak egyszer példányosítható!")


    def __init__(self, scene):
        """
        LightLibraly inicilializálása
        """
        self.__maxLights        = int(glGetIntegerv(GL_MAX_LIGHTS))             #:@ivar: A rendszerben elérhető maximális fényforrások száma
        self.__lightSet         = None                                          #:@ivar: OpenGL fényforrás azonosítók halmaza
        self.__linkedLights     = {}                                            #:@ivar: Felhasznált aonosítók listálya
        self.__lighting         = False                                         #:@ivar: C{True} ha a világítás be van kapcsolva különben C{False}
        self.__scene            = scene                                         #:@ivar: Hivatkozás a fő színre

        lightList = []
        for i in xrange(self.__maxLights):
            lightList.append(GL_LIGHT0 + i)

        self.__lightSet = frozenset(lightList)
        
        self.turnOnLights()
        print "inited Lights"


    @classmethod
    def getInstance(cls):
        """
        Az egyetlen GfxContext példány lekérése

        @return:    LightLibraly példány
        @rtype:     C{LightLibraly}
        """
        return cls._instance


    def globalAmbient(self, value):
        """
        Globális fények beállítása

        @param  value:  Színértékek [R,G,B,a] formában
        @type   value:  C{list}
        """
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, value)


    def addLight(self):
        """
        Új fényforrás regisztrálása
        A fényforrások száma nem haladhatja meg a rendser által támogatott
        míximális értéket.

        @return:    A létrejött fény objektum
        @rtype:     C{LightObject}

        @raise: C{IloError}
        """
        unLinkedLights = tuple(self.__lightSet - set(self.__linkedLights.keys()))
        if len(unLinkedLights) > 0:
            key = unLinkedLights[0]
            light = LightObject(key, 'omni')
            self.__linkedLights[key] = light
            return light
        else:
            raise IloError("Nincs több fényforrás! max: %s" % str(self.maxLights))
            

    def getLinkedLightsIDs(self):
        """
        A felhasznált fényforrásdok azonosítóinak listáját adja vissza

        @return: Felhasznált fényforrás azonosítók listája
        @rtype:  C{list}
        """
        return self.__linkedLights.keys()


    def getLinkedLightObjects(self):
        """
        A felhasznált fényforrásdok azonosítókhoz kötött fényforrás objektumok
        (C{LightObject}) listáját adja vissza

        @return: Felhasznált fényforrás azonosítókhoz kötött fény objektumok
                 listája
        @rtype:  C{list}
        """
        return self.__linkedLights.values()


    def removeLight(self, lightID):
        """
        Használatban évő fényforrás törlése azonosító alapján

        @param  lightID:    Egyedi OpenGL-es fényforrás azonosító
        @type   lightID:    C{int}
        """
        if lightID in self.__linkedLights:
            del self.__linkedLights[lightID]


    def turnOnLights(self):
        """
        Fények rendszer szintű kikapcsolása
        """
        self.__lighting = True
        glEnable(GL_LIGHTING)
        glEnable(GL_COLOR_MATERIAL)


    def turnOffLights(self):
        """
        Fények rendszerszintű bekapcsolása
        """
        self.__lighting = False
        glDisable(GL_LIGHTING)
        glDisable(GL_COLOR_MATERIAL)


    def switchLight(self):
        """
        Fények rendszerszintű ki/bekapcsolása
        """
        if self.__lighting:
            self.turnOffLights()
        else:
            self.turnOnLights()

    @property
    def lightning(self):
        """Fények használata be van kapcsolva ha C{True} különben C{False}"""
        return self.__lighting

    @property
    def maxLight(self):
        """Fényforrások maximális száma"""
        return self.__maxLights

    @property
    def availableLightsNumber(self):
        """Elérhető fényforrások száma"""
        return len(unLinkedLights)


################################################################################


class LightObject(RenderObject):
    """
    Specializált C{RenderObject} mely egy fényforrást reprezentál

    @see:   RenderObject
    """

    __slots__ = RenderObject.__slots__ + \
                ('__glLightId','__active', 'lightType', 'diffuse', 'ambient',
                 'specular', 'lightIntesity', '__dirLight', '__spot',
                 '__spotDirection', '__spotCutOff')

    LIGHT_TYPE_OMNI = "omni"
    LIGHT_TYPE_SPOT = "spot"

    def __init__(self, lightId, type, name="", coord=[0.,0.,0.], \
                 diffuse=[0,0,0,1], ambient=[0,0,0,1], specular=[0,0,0,1], \
                 intesity=1.0, geometry=None):
        """
        LightObject inicializálása

        @param  lightId:    A fényforrás egyedi openGL azonosítója
        @type   lightId:    C{GLuint}
        @param  type:       A fényforrás típusa {omni|spot}
        @type   type:       C{String}
        @param  name:       A fényforrás megnevezése I{(Opcionális)}
        @type   name:       C{String}
        @param  coord:      A fényforrás koordinátái
        @type   coord:      C{list}
        @param  diffuse:    A fényforrás diffuse színérétkei
        @type   diffuse:    C{list}
        @param  ambient:    A fényforrás ambient színérétkei
        @type   ambient:    C{list}
        @param  specular:   A fényforrás specular színérétkei
        @type   specular:   C{list}
        @param  intesity:   A fényforrás intenzitása
        @type   intesity:   C{float}
        @param  geometry:   A fényforrst szimbolizáló gerfikus objektum I{(Opcionális)}
        @tpye   geometry:   C{Mesh}
        """
        RenderObject.__init__(self, name, geometry, None)


#        if not isinstance(lightLib, LightLibraly):
#            raise IloError("Csak a LightLibraly osztály példányosíthatja")
        self.__glLightId        = lightId                                       #:@ivar: A fényforrás OpenGL-es belső azonosítója
        self.__active           = True                                          #:@ivar: C{True} ha be van kapcsolva különben C{False}

        self.lightType          = type                                          #:@ivar: Fényforrás típusa {omni|spot}
        self.diffuse            = diffuse                                       #:@ivar: A fényforrás diffuse színérétkei
        self.ambient            = ambient                                       #:@ivar: A fényforrás ambient színérétkei
        self.specular           = specular                                      #:@ivar: A fényforrás specular színérétkei
        self.lightIntesity      = 1.0                                           #:@ivar: A fényforrás intenzitása
        self.__dirLight         = 1.0                                           #:@ivar: A fényforrás iránya
        self.__spot             = False                                         #:@ivar: Spot fény tuljdonságok bekapcsolása
        self.__spotDirection    = Vector3([0.0,0.0,-1.0])                       #:@ivar: A spot fény iránya
        self.__spotCutOff       = 5                                             #:@ivar: A spot fény levágása azaz nyílásszöge


    def render__(self):
        """
        Fényforrás leképezése.
        Koordináták és színek beállítása.
        """

        if self.__active:
            glLightfv(self.__glLightId, GL_POSITION, self._coord.tolist()+[1.0])
            glLightfv(self.__glLightId, GL_DIFFUSE,  self.diffuse)
            glLightfv(self.__glLightId, GL_AMBIENT,  self.ambient)
            glLightfv(self.__glLightId, GL_SPECULAR, self.specular)
            if self.__spot:
                glLightfv(self.__glLightId, GL_SPOT_DIRECTION, self.__spotDirection)
                glLightf (self.__glLightId, GL_SPOT_CUTOFF,    self.__spotCutOff)
                glLightf (self.__glLightId, GL_SPOT_EXPONENT,  100.0)

        glPushAttrib(GL_ALL_ATTRIB_BITS)
        glDisable(GL_LIGHTING)
        glPushMatrix()

        glTranslate(*self._coord )
        glRotate(self._angle.x,1.0, 0.0, 0.0)
        glRotate(self._angle.y,0.0, 1.0, 0.0)
        glRotate(self._angle.z,0.0, 0.0, 1.0)
        glScale(*self._scale)

        glBegin(GL_POINTS)
        glColor(1.0, 1.0, 1.0)
        glVertex3fv(self._coord)
        if self.__spot :
            glVertex3fv(self.__spotDirection)
        glEnd()

        glPopMatrix()
        glPopAttrib(GL_ALL_ATTRIB_BITS)



    def setSpot(self, spotDir=[0,0,0], cutOff=30):
        """
        Spot fény beállítása

        @param  spotDir:    A spot fény iránya
        @type   spotDir:    C{list}
        @param  cutOff:     A spot nyílásszöge fokban
        @type   cutOff:     C{float}
        """
        self.__spotDirection = spotDir
        self.__spotCutOff = cutOff
        self.__spot = True


    def unsetSpot(self):
        """
        A spot fényforrás visszaállítása 'normál' pontszerű fényre
        """
        self.__spotDirection = None
        self.__spotCutOff = None
        self.__spot = False
        self.__setNewLightValues()


    def added__ (self, parent, scene):
        """
        A fényforrást hozzáadtuk egy másik C{RenderObject}-hez

        @param  parent: A fényforrás szülő elem
        @type   parent: C{RenderObject}
        @parem  scene:  A fő szín
        @type   scene:  C{RenderScene}
        """
        self.enable()
        self.__setNewLightValues()
        RenderObject.addedToScene__(self, parent, scene)


    def addedToScene__ (self, scene):
        """
        A fényforrást hozzáadtuk a fő színhez

        @parem  scene:  A fő szín
        @type   scene:  C{RenderScene}
        """
        self.enable()
        RenderObject.addedToScene__(self, scene)


    def removed__ (self):
        """
        A fényforrást töröltük egy másik C{RenderObject}-ból
        """
        self.disable()
        RenderObject.removed__(self)


    def removedFromScene__(self):
        """
        A fényforrást töröltük a fő színről
        """
        self.disable()
        RenderObject.removedFromScene__(self)


#    def __setattr__(self, name, value):
#        """
#        Minden fényforrás paraméter változáskor megváltoztatjuk az OpenGL
#        beállításokat is.
#        """
#        self.__dict__[name] = value

    def enable (self):
        """
        Fényforrás bekapcsolása
        """
        self.__active = True
        glEnable(self.__glLightId)


    def disable(self):
        """
        Fényforrás kikapcsolása
        """
        self.__active = False
        glDisable(self.__glLightId)


    @property
    def spotDirection(self):
        """Spot fény iránya"""
        return self.__spotDirection

    @spotDirection.setter
    def spotDirection(self, value):
        self.__spotDirection = Vector3(value)
        self.__spot = True

    @property
    def spotCutOff(self):
        """Spot fény nyílásszöge fokban"""
        return self.__spotCutOff

    @spotCutOff.setter
    def spotCutOff (self, value):
        self.__spotCutOff = value
        self.__spot = True

    @property
    def isSpot(self):
        """C{True} ha a fényforrás típusa C{Spot} különben C{False}"""
        return self.__spot
