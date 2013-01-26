# -*- coding: utf -*-

__author__="Vadasz Laszlo"
__date__ ="2009.08.25. 12:13:34"


"""
Eseményvezérléssel kapcsolatos osztályokat tartlmazó modul
Ezek a osztályok alakotják az eseményvezérlés alapjait
"""

class   EventDispatcher(object):
    """
    Eseményvezérlő ostály
    Tárolja és meghívja a hozá kapcsolt eseménykezelőket a megefelő esemény
    bekövetkezése után.
    """

    __slots__ =  ('_target', '__eventList')

    def __init__(self):
        """
        Az eseményvezérlő inicilaizálása
        """
        self._target = self                                                     #:@ivar: Az esemény dobásának helye
        self.__eventList = {}                                                   #:@ivar: Eseményeket tároló lista


    def addEventListener(self, type, listener):
        """
        Új eseményfigyelő hozzáfűzése az eseménylistához
        Egy esemény tpíushoz több eseményvezérlő is felvehető.

        @param type:     Az esemény típusa
        @type  type:     C{String}
        @param listener: Az eseménykezelő függvény
        @type  listener: C{Function(Event)}
        """
        if type not in self.__eventList :
            self.__eventList[type] = []
        if listener not in self.__eventList[type] :
            self.__eventList[type].append(listener)


    def dispatchEvent(self, event):
        """
        Esemény dobás.
        Ha az eseményvezérlőlistában szerepel a megadott esemény típusa
        akkor ez az esemény átadódik minden a típusához kapcsolt
        eseménykezelőnek

        @param  event:  A dobott esemény adatait tároló esemény objektum
        @type   event:  C{Event}
        """
        event._target = self._target
        if event.type in self.__eventList:
            for listener in self.__eventList[event.type]:
                listener(event)


    def hasEventListener(self, type):
        """
        Ellenőrzi, hogy a megadott eseménytípus fel van-e véve az
        eseményvezérlő listába

        @param  type:   A keresett esemény típusa
        @type   type:   C{String}

        @return:  C{True} ha létezik van ilyen eseménykezelő, különben C{False}
        @rtype:   C{Bool}
        """
        return type in self.__eventList


    def removeEventListener(self, type, listener):
        """
        Esemény törlése az esemény figyelők közül

        @param  tpye:       Az esemény típusa
        @type   type:       C{String}
        @param  listener:   Az eseménykezelő függvény
        @type   listener:   C{Function(Event)}
        """
        if type in self.__eventList:
            if listener in self.__eventList[type]:
                del self.__eventList[type][self.__eventList[type].index(listener)]

    def __str__(self):
        return "Event dispatcher, target: %s" % (self._target)



################################################################################


#{ Eseményobjektumok
class Event(object):
    """
    Általános esemény
    Tartalmazza az eseményt kiváltó objektum hivatkozását és az esemény típusát

     - Inicializálás vége
     - OpenGL inicilizálás vége
     - Folyamat befejeződött
     - Grafikai elem hozzádása a másikhoz
     - Grafikai elem hozzádása a színhez
     - Grafikai elem törlése egy másikból
     - Grafikai elem törlése a színről
     - Grafiaki elem leképezése
     - Képkocka ugrás
     - Bezárás
    """

    __slots__ = ('_target', '_type')

    INIT                = "init"
    GL_INIT             = "glInit"
    COMPLETE            = "complete"
    ADDED               = "added"
    ADDED_TO_SCENE      = "addedToScene"
    REMOVED             = "removed"
    REMOVED_FROM_SCENE  = "removedFromScene"
    RENDERED            = "rendered"
    ENTER_FRAME         = "enterFrame"
    CLOSE               = "close"

    def __init__(self, type):
        """
        Esemény objektum inicializálása

        @param  type:   Az esemény típusa
        @type   tpye:   C{String}
        """
        self._target = None                                                     #:@ivar: Az esemény kiváltója
        self._type = type                                                       #:@ivar: Az esmény típusa


    def clone(self):
        """
        Esemény klónozása

        @return:    Klónozott esemény
        @rtype:     C{Event}
        """
        return Event(self.type, self.bubbles)


    def __str__(self):
        return "Event @ %s", self._type

    @property
    def target(self):
        """Az eseményt kiváltó objektum"""
        return self._target

    @property
    def type(self):
        """Esemény típusa"""
        return self._type



################################################################################



class ElementEvent(Event):
    """
    Grafikus objektum által kiváltott esemény
    Az esemény kiváltó grafikus objektum hivatkozását is tarolja

     - Az elem leképezése befejeződött

    @see Event
    """

    __slots__ = Event.__slots__ + ('_element',)

    RENDERED = "rendered"

    def __init__(self, type, element):
        """
        Esemény objektum inicialiálása

        @param  type:       Az esemény típusa
        @type   type:       C{String}
        @param  element:    Az eseményhez kötődő grafikus elem
        @type   element:    C{RenderObject}
        """
        Event.__init__(self, type)
        self._element = element                                                 #:@ivar: Az eseményt kiváltó grafikus objektum

    def clone(self):
        """
        Esemény klónozása

        @return:    Klónozott esemény
        @rtype:     C{ElementEvent}
        """
        return ElementEvent(self.type, self.element)

    def __repr__(self):
        return "ElementEvent @ %s", self._type


    @property
    def element(self):
        """Az eseményt kiváltó elem"""
        return self._element



################################################################################



class MouseEvent(Event):
    """
    Egér műveletek által  kiváltott esemény
     - bal egérgomb lenyomása
     - bal egérgomb felengedése
     - az egér ráhúzása valamire
     - az egér lehúzása valmiről
     - egér mozgatása
     - egér görgő haszálata
    """

    __slots__ = Event.__slots__ + ('_pos', '_delta', '_button', '_wheel',
                                   '_altKey', '_ctrlKey', '_shiftKey')

    ROLL_OVER =     "rollOver"
    ROLL_OUT =      "rollOut"
    CLICK =         "leftClick"
    RELEASE =       "leftRelease"
    MOVE =          "move"
    WHEEL =         "wheel"

    def __init__(self, type, button, pos, delta, wheel=0, altKey=False,
                 ctrlKey=False, shiftKey=False):
        """
        Esemény objektum inicialiálása

        @param  type:       Az esemény típusa
        @type   type:       C{String}
        @param  button:     Az egérgomb kódja
        @type   button:     C{int}
        @param  pos:        Az egérmutató x,y koordinátája a képernyőn
        @type   pos:        C{Vector2}
        @param  delta:      Az egérmutató relatív x,y pozíciója az utólsó
                            állípothoz képet
        @type   delta:      C{Vector2}
        @param  wheel:      Egérgörgő állapota (alapesetben: 0)
        @type   wheel:      C{int}
        @param  altKey:     Le van-e nyomva az Alt billentyű C{True} ha igen
                            különben C{False}
        @type   altKey:     C{Bool}
        @param  ctrlKey:    Le van-e nyomva az Ctrl billentyű C{True} ha igen
                            különben C{False}
        @type   ctrlKey:    C{Bool}
        @param  shiftKey:   Le van-e nyomva az Shift billentyű C{True} ha igen
                            különben C{False}
        @type   shiftKey:   C{Bool}
        """

        Event.__init__(self, type)
        self._pos      = pos                                                    #:@ivar: Az egérmutató poziciója a képernyőn
        self._delta    = delta                                                  #:@ivar: Az egérmutató relatív pozíciója
        self._button   = button                                                 #:@ivar: A lenyomott gomb kódja
        self._wheel    = wheel                                                  #:@ivar: Az egérgörgő elmozdulása
        self._altKey   = altKey                                                 #:@ivar: Az Alt gomb állapota, azaz le van-e nyomva
        self._ctrlKey  = ctrlKey                                                #:@ivar: Az Ctrl gomb állapota, azaz le van-e nyomva
        self._shiftKey = shiftKey                                               #:@ivar: Az Shift gomb állapota, azaz le van-e nyomva

    def clone(self):
        """
        Esemény klónozása

        @return:    Kónozott esemény
        @rtype:     C{MouseEvent}
        """
        return MouseEvent(self.type, self.pos, self.delta, self.button, self.wheel,
                          self.altKey, self.ctrlKey, self.shiftKey)

    def __str__(self):
        return "MouseEvent @ %s", self._type

    @property
    def pos(self):
        """Az egér mutató abszolut pozíciója"""
        return self._pos

    @property
    def delta(self):
        """Az egyérmutató relatív pozíciója"""
        return self._delta

    @property
    def button(self):
        """A lenyomott egérgomb kódja"""
        return self._button

    @property
    def wheel(self):
        """A görgetés mértéke"""
        return self._wheel

    @property
    def altKey(self):
        """Alt gomb állapota"""
        return self._altKey

    @property
    def ctrlKey(self):
        """Ctrl gomb állapota"""
        return self._ctrlKey

    @property
    def shiftKey(self):
        """Shift gomb állapota"""
        return self._shiftKey



################################################################################



class KeyboardEvent(Event):
    """
    Billenyű lenyomáskor keletkező esemény

     - Billentyű lenyomás
     - Billentyű felengedés
    """

    __slots__ = Event.__slots__ + ('_key', '_altKey', '_ctrlKey', '_shiftKey')

    PRESS =     "press"
    RELEASE =   "release"

    def __init__(self, type, key, altKey = False, ctrlKey = False, shiftKey = False):
        """
        Esemény objektum inicialiálása
        
        @param  type:       Az esemény típusa
        @type   type:       C{String}
        @param  key:        A leütött billentyű kódja
        @type   key:        C{int}
        @param  altKey:     Le van-e nyomva az Alt billentyű C{True} ha igen
                            különben C{False}
        @type   altKey:     C{Bool}
        @param  ctrlKey:    Le van-e nyomva az Ctrl billentyű C{True} ha igen
                            különben C{False}
        @type   ctrlKey:    C{Bool}
        @param  shiftKey:   Le van-e nyomva az Shift billentyű C{True} ha igen
                            különben C{False}
        @type   shiftKey:   C{Bool}
        """
        Event.__init__(self, type)
        self._key      = key                                                    #:@ivar: A lenyomott billentyű kódja
        self._altKey   = altKey                                                 #:@ivar: Az Alt gomb állapota, azaz le van-e nyomva
        self._ctrlKey  = ctrlKey                                                #:@ivar: Az Ctrl gomb állapota, azaz le van-e nyomva
        self._shiftKey = shiftKey                                               #:@ivar: Az Shift gomb állapota, azaz le van-e nyomva


    def clone(self):
        """
        Esemény klónozása

        @return:    Kónozott esemény
        @rtype:     C{KeyboardEvent}
        """
        return KeyboardEvent(self._type, self._key, self._altKey, self._ctrlKey,
                             self._shiftKey)

    def __str__(self):
        return "KeyboardEvent @ %s", self._type


    @property
    def key(self):
        """A leütött beillentyű kódja"""
        return self._key

    @property
    def altKey(self):
        """Alt gomb állapota"""
        return self._altKey

    @property
    def ctrlKey(self):
        """Ctrl gomb állapota"""
        return self._ctrlKey

    @property
    def shiftKey(self):
        """Shift gomb állapota"""
        return self._shiftKey



################################################################################


class WindowEvent(Event):
    """
    Billentyűzet esemény
    """

    __slots__ = Event.__slots__ + ('_x', '_y', '_width', '_height')

    RESIZE =    "resize"

    def __init__(self, type, x, y, width, height):
        """
        Esemény objektum inicialiálása

        @param  type:   Az esemény típusa
        @type   type:   C{String}
        @param  x:      Az ablak X koordinátája
        @type   x:      C{int}
        @param  y:      Az ablak Y koordinátája
        @type   y:      C{int}
        @param  width:  Az ablak szélessége
        @type   width:  C{int}
        @param  height: Az ablak magassága
        @type   height: C{int}
        """
        Event.__init__(self, type)
        self._x = x                                                             #:@ivar: Az ablak x koordinátája
        self._y = y                                                             #:@ivar: Az ablak y koordinátája
        self._width = width                                                     #:@ivar: Az ablak szélessége
        self._height = height                                                   #:@ivar: Az ablak magassága


    def clone(self):
        """
        Esemény klónozása

        @return:    Kónozott esemény
        @rtype:     C{WindowEvent}
        """
        return KeyboardEvent(self._type, self._x, self._y, self._width,
                             self._height)


    def __str__(self):
        return "WindowEvent @ %s", self._type


    @property
    def x(self):
        """Az ablak aktuális x koordinátája"""
        return self._x

    @property
    def y(self):
        """Az ablak aktuális y koordinátája"""
        return self._y

    @property
    def width(self):
        """Az ablak aktuális szélessége"""
        return self._width

    @property
    def height(self):
        """Az ablak aktuális magassága"""
        return self._height

#}
