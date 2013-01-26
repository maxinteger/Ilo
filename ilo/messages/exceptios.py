# -*- coding: utf -*-

__author__="Vadasz Laszlo"
__date__ ="2009.08.27. 12:22:11"


"""
Ilo hiba és kivétel osztályokat tarlamazó modul
"""

class StaticClassError(Exception):
    """
    Nem példányosítható osztály, mely csak statikus metódusokat és adattagokat
    tartalmaz. Példányosításkor keletkező hiba.
    """
    pass

class SingletonClassError (Exception):
    """
    Egyszer példányosítható osztály (Singleton class) újboli példányosításakor
    keletkező hiba.
    """
    pass

class StaticClassError (Exception):
    """
    Statikus osztály példányosításakor keletkező hiba.
    """
    pass


class IloError (Exception):
    """
    Általános az Ilo motor futása közbe keletkező hiba.
    """
    pass

class IloNumberError (IloError):
    """
    Számformátum hiba.
    """
    pass

class IloInitError (IloError):
    """
    A motor vagy egyéb elemek inicializálása közben keletkező hiba.
    """
    pass

class IloExtensionError(IloError):
    """
    A futtató rendszer által nem támogatott funkciók vizsgálatakor illetve
    azok végrehajtása közben keletkező hiba.
    """
    pass

class IloLibralyErro(IloError):
    """
    Ilo könyvári művelet közben keletkező hiba
    """
    pass


class IloRenderError (IloError):
    """
    Leképezés közben keletkező hiba
    """
    def __init__(self, element, value):
        self.value = value
        self.element = element

    def __str__(self):
        return repr(self.value + self.element)
