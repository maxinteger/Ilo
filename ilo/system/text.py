# -*- coding: utf -*-

__author__="Vadasz Laszlo"
__date__ ="2010.02.17. 6:50:39"
__all__ = ["Text"]


"""
A textúra alpú szövegobjektumokat vezértlő osztályokat tartalmazzó modul
"""

class Text(object):
    """
    Font map szöveg kiíratást vezérlő szingleton oszály

    Egy listába veszi fel a kiíratandó sövegeket és azok adatait
    majd ezt egyszerre képezi le a GFX osztály
    """

    _instance = None                                                            #:@cvar: Az osztály egyetelen példánya

    __slots__ = ('__textList')

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Text, cls).__new__( cls, *args, **kwargs)
            return cls._instance
        else:
            raise SingletonClassError("Csak egyszer példányosítható!")

    def __init__(self):
        """
        Text iniclializálása
        """
        self.__textList = []                                                    #:@ivar: szöveg objektumok listája


    @classmethod
    def getInstance(cls):
        """
        Az osztály egyetlen létező példányát adja vissza

        return: Osztály példány
        rtype:  C{Text}
        """
        return cls._instance


    def addText(self, x, y, text, color=[1.,1.,1.,1.], scale=[1.,1.,1.], fontSet=0):
        """
        Új szöveg objektum hozzáadása a listához

        @param  x:       A szöveg x koordinátái a képernyőn
        @type   x:       C{int}
        @param  y:       A szöveg y koordinátái a képernyőn
        @type   y:       C{int}
        @param  text:    A kiíratandó szöveg
        @type   text:    C{string}
        @param  color:   A szöveg színe
        @type   color:   C{list}
        @param  scale:   A szöveg skálázása
        @type   scale:   C{list}
        @param  fontSet: Betűkészlet (0 vagy 1)
        @type   fontSet: C{int}

        @return: Szövegobjektum
        @rtype:  C{LineText}
        """
        line = LineText(x, y, text, color, scale, fontSet)
        self.__textList.append(line)
        return line


    def removeText(self, text):
        """
        Felvett szöveg törlése
        
        @param  text:   Törli a listából a megadott hivatkozást
        @type   text:   C{string}
        """
        del self.__textList[self.__textList.index(text)]


    def removeAll(self):
        """
        Minden elem törlése
        """
        self.__textList = []


    @property
    def textList(self):
        """Szövegobjektumok listája"""
        return self.__textList



class LineText(object):
    """
    Szövegobjektum a leképezendő szövegek kezelésére
    """

    __slots__ = ('x', 'y', 'text', 'color', 'scale', 'fontSet')

    def __init__(self, x, y, text, color, scale, fontSet):
        """
        LineText inicilaizálása

        @param  x:       A szöveg x koordinátái a képernyőn
        @type   x:       C{int}
        @param  y:       A szöveg y koordinátái a képernyőn
        @type   y:       C{int}
        @param  text:    A kiíratandó szöveg
        @type   text:    C{string}
        @param  color:   A szöveg színe
        @type   color:   C{list}
        @param  scale:   A szöveg skálázása
        @type   scale:   C{list}
        @param  fontSet: Betűkészlet (0 vagy 1)
        @type   fontSet: C{int}
        """
        self.x        = x                                                       #:@ivar: A szöveg x koordinátái a képernyőn
        self.y        = y                                                       #:@ivar: A szöveg y koordinátái a képernyőn
        self.text     = text                                                    #:@ivar: A kiíratandó szöveg
        self.color    = color                                                   #:@ivar: A szöveg színe
        self.scale    = scale                                                   #:@ivar: A szöveg skálázása
        self.fontSet  = fontSet                                                 #:@ivar: Betűkészlet (0 vagy 1)
