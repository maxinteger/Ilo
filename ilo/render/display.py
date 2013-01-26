# -*- coding: utf -*-

__author__="Vadasz Laszlo"
__date__ ="2009.08.27. 11:38:25"

from ilo.config import *
from OpenGL.GL import *

from ilo.structs.vector import *
from ilo.messages.events import *
from ilo.messages.exceptios import *
from ilo.system.material import Texture


"""
Ebben a modulban a grafikus objektum hierarchia alap osztályai helyezkednek el.
"""

class RenderObject(EventDispatcher):
    """
    A grafikus objektum hierarchia alaposztálya
    Trolja az objektum geometriáját és a hozzátartozó anyagjellemzőket
    Továbbá a megadható az objekt pozícciója elforgatása és méretezése
    Szintén itt kerül sor az objektumok leképezésére és a hierarchia műveletek
    kezelésére is.
    """

    __slots__ = EventDispatcher.__slots__ + \
                ('_id', '_name', '_parent', '_scene',
                 '_coord', '_scale', '_angle',
                 '_geometry', '_material',
                 '_showNormals', 'visible')

    def __init__(self, name="", geometry=None, material=None):
        """
        Render objektum inicilaizálása

        @param  name:       Az objektum neve I{(Opcionális)}
        @type   name:       C{String}
        @param  geometry:   Az objektum geometriai adatai I{(Opcionális)}
        @type   geometry:   C{Mesh}
        @param  material:   Az objektum anyagmintája I{(Opcionális)}
        @type   material:   C{Material}
        """
        EventDispatcher.__init__(self)
        self._id            = ""                                                #:@ivar: Egyedi objektum azonosító
        self._name          = name                                              #:@ivar: Az objektum neve
        self._parent        = None                                              #:@ivar: Az objektum szülőelemét adja meg
        self._scene         = None                                              #:@ivar: Hivatkozás a C{scene}-re

        self._coord         = Vector3([0.0]*3)                                  #:@ivar: Obejktum koordináták
        self._scale         = Vector3([1.0]*3)                                  #:@ivar: Objektu skáláz értékei
        self._angle         = Vector3([0.0]*3)                                  #:@ivar: Objektum elforgati értékei

        self._geometry      = geometry                                          #:@ivar: Mesh objektum
        self._material      = material                                          #:@ivar: A geometrea anyagmintája

        self._showNormals   = False                                             #:@ivar: Mesh normálvektorok megjelenítése
        self.visible        = True                                              #:@ivar: Láthatóság

        if geometry != None and Config.getValue("display.normalvectors"):
           self._geometry.showNormalVectors()


    #Implement IRenderable
    def render__(self):
        """
        Grafikus objektum pozicionálása textúra kötése és leképezés
        """
        glPushMatrix()
        glTranslate(*self._coord )
        glRotate(self._angle.x,1.0, 0.0, 0.0)
        glRotate(self._angle.y,0.0, 1.0, 0.0)
        glRotate(self._angle.z,0.0, 0.0, 1.0)
        glScale(*self._scale)
        
        if self.visible and self._geometry != None:
            glLoadName(self._id)
            if self._material != None:
                self._material.bindMaterial()
            else:
                Texture.unbindTexture()

            self._geometry.renderMesh()

            if self._showNormals:
                self._geometry.renderNormalVectors()

            if self.hasEventListener(Event.RENDERED):
                self.dispatchEvent(Event(Event.RENDERED))
        glPopMatrix()

    @property
    def id(self):
        """Egyedi objektum azonosító"""
        return self._id

    @property
    def name(self):
        """Objetum neve"""
        return self._name

    @property
    def parent(self):
        """Hivatkozás a szülő objektumra"""
        return self._parent

    @parent.setter
    def parent(self, value):
        if isinstance(value, RenderObject):
            self.scene = value
        else:
            raise IloError("A megadott objektum nem lehet szülőelem!")

    @property
    def scene(self):
        """Hivatkozás a főszínre"""
        return self._scene

    @scene.setter
    def scene(self, value):
        self._scene = value

    @property
    def coord(self):
        """Objektumkoordináták"""
        return self._coord

    @coord.setter
    def coord(self, value):
        self._coord = Vector3(value)

    @property
    def scale(self):
        """Objetum méretezés"""
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = Vector3(value)

    @property
    def angle(self):
        """Objektum elforgatása"""
        return self._angle

    @angle.setter
    def angle(self, value):
        self._angle = Vector3(value)

    @property
    def geometry(self):
        """Az objektum geometriaiája"""
        return self._geometry

    @property
    def material(self):
        """Az objektum anyagjellemzői"""
        return self._material

    @property
    def showNormals(self):
        """Az objektum normál vektorjainak megjelenítése"""
        return self._showNormals

    @showNormals.setter
    def showNormals(self, value):
        self._showNormals = value

        if self._geometry != None:
            if value:
                self._geometry.showNormalVectors()
            else:
                self._geometry.hideNormalVectors()

    def added__ (self, parent, scene):
        """
        A grafikus elemet hozzáadtuk egy elem konténerhez
        """
        self.parent = parent
        self.scene = scene
        if self.hasEventListener(Event.ADDED):
            self.dispatchEvent(Event(Event.ADDED))

    def addedToScene__ (self, scene):
        """
        Az elemet hozzáadtuk a főszínhez
        """
        self.parent = self._scene = scene
        if self.hasEventListener(Event.ADDED_TO_SCENE):
            self.dispatchEvent(Event(Event.ADDED_TO_SCENE))

    def removed__ (self):
        """
        Az elemet töröltük az elemkonténerből
        """
        if self.hasEventListener(Event.REMOVE):
            self.dispatchEvent(Event(Event.REMOVE))

    def removedFromScene__(self):
        """
        Az elemet törötltük a főszínről
        """
        if self.hasEventListener(Event.REMOVED_FROM_SCENE):
            self.dispatchEvent(Event(Event.REMOVED_FROM_SCENE))

    def __str__ (self):
        return "RenderObject %s" % (name)
#    def __setattr__ (self, name, value):
#        self.__dict__[name] = value
#        if name in ['coord','angle', 'scale'] :
#            print self.name, value, self.__dict__[name]

#-------------------------------------------------------------------------------



class RenderObjectContainer(RenderObject):
    """
    Specilaizált C{RenderObject} mely megjelenítés mellett további
    C{RenderObject}-eket és/vagy C{RenderObjectContainer}-eket képes tárolni
    és kezelni
    """

    __slots__ = RenderObject.__slots__ + ('elementList', )

    def __init__(self, name="", geometry=None, material=None):
        """
        RenderObjectContainer inicilaizálása

        @param  name:       Az objektum neve I{(Opcionális)}
        @type   name:       C{String}
        @param  geometry:   Az objektum geometriai adatai I{(Opcionális)}
        @type   geometry:   C{Mesh}
        @param  material:   Az objektum anyagmintája I{(Opcionális)}
        @type   material:   C{Material}
        """
        RenderObject.__init__(self, name, geometry, material)
        self.elementList = {}
        self._scene = None

    def addElement(self, element, name = ""):
        """
        Új elem hozzáadása a konténerhez

        @param  element:    A hozzáadandó elem
        @type   element:    C{RenderObject}
        @param  name:       Az elem neve a konténerben
        @type   name:       C{string}

        @return:    A konténer hivatkozása
        @rtype:     C{RenerObjectContainer}
        """
        if not isinstance(element, RenderObject):
            raise ElementError("Csak RenderObject típsú elemek adhatók a hiearchiához.", element)
        elif element not in self.elementList:
            self.elementList[element] = name
            element.scene = self._scene
            element.added__(self, self._scene)
            return self
        else:
            raise ElementError("Az elem már hozzá lett adva", element)

    def getElementsByName(self, name):
        """
        A konténerben lévő megadott nevű elem lekérése

        @param  name:   Az elem neve
        @type   name:   C{string}

        @return:    A megadott névvel rendelkező elemek listája
        @rtype:     C{list}
        """
        elements = []
        for element, eName in self.elementList.iteritems():
            if name == eName:
                elements.append(element)
        return elements

    def removeElement(self, element):
        """
        Elem törlése a rámutató hivatkozás alapján

        @param  element:    A törlendő elem hivatkozás
        @type   element:    C{RenderObject}

        @return:    A törlendő elem hivatkozása
        @rtype:     C{RenderObject}
        """
        if element in self.elementList:
            element.removed__()
            del self.elementList[element]
            return element
        else:
            raise ElementError("Nincs ilyen elem", element)

    def removeElementsByName(self, name):
        """
        A megadott névvel megegyező nevű objektumok törlése

        @param  name:   A keresett név
        @type   name:   C{string}

        @return:    A törölt elemek listája
        @rtype:     C{list}
        """
        elements = self.getElementsByName(name)
        for element in elements:
            self.removeElement(element)



    def render__(self):
        """
        A konténer poziciónálása méretezése és forgatása
        A tárolt elemek leképezése
        végül a saját geometria leképezése
        """
        glPushMatrix()
        glTranslate(*self._coord)
        glRotate(self._angle[0],1.0, 0.0, 0.0)
        glRotate(self._angle[1],0.0, 1.0, 0.0)
        glRotate(self._angle[2],0.0, 0.0, 1.0)
        glScale(*self._scale)
        
        for element in self.elementList:
            element.render__()

        if self.visible and self._geometry != None:
#            glLoadName(self._id)

            if self._material != None:
                self._material.bindMaterial()
            else:
                Texture.unbindTexture()

            self._geometry.renderMesh()

        glPopMatrix()

        if self.hasEventListener(Event.RENDERED):
            self.dispatchEvent(Event(Event.RENDERED))

    @property
    def scene(self):
        """Hivatkozás a főszínre"""
        return self._scene

    @scene.setter
    def scene(self, value):
        self._scene = value
        for element in self.elementList:
            element.scene = value

#-------------------------------------------------------------------------------


class RenderScene(RenderObjectContainer):
    """
    Specializált C{RenderObjectContainer} mely a fő tároló azaz a fő szín
    feladatat látja el.
    Ebből az objektumból csak egy van és nincs szülője.
    Továbbá minden gyeremek eleme tatalmaz egy közvetlen hivatkozást a
    fő színre
    """

    __slots__ = RenderObjectContainer.__slots__

    def __init__(self):
        """
        RenderScene inicializálása
        """
        RenderObjectContainer.__init__(self)


    def addElement(self, element, name = ""):
        """
        Új elem hozzáadása a fő színhez.
        Hiba keletkezik ha az adott elemet többször adjuk hozzá

        @param  element:    A hozzáadandó elem
        @type   element:    C{RenderObject}
        @param  name:       Az elem neve I{(Opcionális)}
        @type   name:       C{String}

        @return:    Fő szín
        @rtype:     C{RenderScene}

        @raise:     ElementError
        """
        if not isinstance(element, RenderObject):
            raise ElementError("Csak RenderObject típsú elemek adhatók a " + \
                               "hiearchiához.", element)
        if element not in self.elementList:
            self.elementList[element] = name
            element.scene = self
            element.addedToScene__(self)
            return self
        else:
            raise ElementError("Az elem már hozzá lett adva", element)


    def removeElement(self, element):
        """
        A már hozzáadott elem törlése.
        Hiba keletkezik ha az adott elem nincs a fő színhez adva

        @param  element:    A törlendő elem
        @type   element:    C{RenderObject}
        """
        if element in self.elementList:
            element.removedFromScene__()
            del self.elementList[element]
        else:
            raise ElementError("Nincs ilyen elem", element)


    @property
    def scene(self):
        """Hivatkozás a főszínre"""
        return self

    #TODO !!!
#    @scene.setter
#    def scene(self, value):
#        RenderObjectContainer.scene = self
