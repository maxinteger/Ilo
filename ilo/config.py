# -*- coding: utf -*-

__author__="Vadasz Laszlo"
__date__ ="2009.07.29. 16:34:35"

import os.path
from stringold import *
from xml.dom.minidom import *
from ilo.messages.exceptios import IloError, StaticClassError
from ilo.messages.exceptios import *


"""
A modul a konfigurációs fájllal kapcsolatos metódusokat tartalmazza.

A konfigurációs fájl XML alpú
"""


class Config(object):
    """
    Konfguráció kezelő

    Feladata:
    Konfigurációs fálok betöltése és kezelése.
    Továbbá egyét státusz információk elmentése és lekérdezése
    """

    configPath = "data/config.xml"                                              #:@cvar: A konfigurációs XML elérési útvonala

    __cfg    = {}                                                               #:@cvar: Konfigurációs  lista
    __status = {}                                                               #:@cvar: Státuszinformációs lista

    def __new__(cls, *args, **kwargs):
        """
        @raise StaticClassError: Az osztály nem példányosítható
        """
        raise StaticClassError("Nem példányosítható!")


    @classmethod
    def __loadDefaultConfig(cls):
        """
        Alapvető és egyben alapértelmezett beállítások betöltése
        """
        cls.__cfg["base.libraly_init"]                      = True

        cls.__cfg["system.stencil_bits"]                    = 8

        cls.__cfg["engine.fps"]                             = 90

        cls.__cfg["render.texture"]                         = True
        cls.__cfg["render.shader"]                          = True

        cls.__cfg["projection.fov"]                         = 50.0
        cls.__cfg["window.width"]                           = 640
        cls.__cfg["window.height"]                          = 480

        cls.__cfg["display.normalvectors"]                  = False


    @classmethod
    def loadConfigXML (cls, xmlFile, reset=True):
        """
        Konfigurációs fájl betöltése

        @param  xmlFile:    A konfigurációs fájl elérési útvonla
        @type   xmlFile:    C{string}
        @param  reset:      C{True} esetén törli a régi kunfugurációs értékekt
                            C{False} esetén pedig összefésüli a régit az újjal.
        @tpye   reset:      C{boolean}
        """

        if reset :
            cls.reset()

        cls.__loadDefaultConfig()

        cls.configPath = xmlFile

        if os.path.exists(xmlFile) and os.path.isfile(xmlFile):
            try:
                file_in = open(xmlFile, "r")

                xData = parse(file_in)
                categoris = xData.getElementsByTagName("category")
                for category in categoris:
                    catName = category.getAttribute("name")
                    for item in category.getElementsByTagName("item"):
                        itemName  = item.getAttribute("name")
                        itemValue = item.getAttribute("value")
                        itemType  = item.getAttribute("type")
                        if itemType == 'int':
                            cls.__cfg[lower(catName+"."+itemName)] = int(itemValue)
                        elif itemType == 'bool':
                            cls.__cfg[lower(catName+"."+itemName)] = lower(itemValue) == 'true'
                        else:
                            cls.__cfg[lower(catName+"."+itemName)] = itemValue
            except IOError as err:
                print "Cinfig Error: " + err

    @classmethod
    def saveConfigXML(cls, xmlFile=None):
        """
        Az Aktuális konfiguráci elmentése
        """
        #TODO configrácisó fájl menétése
        pass


    @classmethod
    def reset(cls):
        """
        Aktuális konfigurációs értékek törlése
        """
        cls.__cfg = {}


    @classmethod
    def getValue(cls, name):
        """
        Konfigurációs érétk lekérdezése

        @param  name:       Konfigurációs érték neve C{[kategória].[név]} formában
        @type   name:       C{string}

        @return:            A névhez tartozó érték
        @rtype:             C{any}
        
        @raise  IloError:   Nemlétező kulcs esetén kivétel keletkezik
        """
        try:
            return cls.__cfg[lower(name)]
        except:
            raise IloError("A megadott paraméter nincs a configurációs listában!: %s" % lower(name))


    @classmethod
    def hasValue(cls, name):
        """
        Létezik-e az adott név a konfigurációs bejegyzések között?

        @param  name:       Konfigurációs érték neve
        @type   name:       C{string}

        @return:            C{True} ha létezik, C{False} ha nem létezik a bejegyzés
        @rtype:             C{bool}
        """
        return lower(name) in cls.__cfg


    @classmethod
    def setStatus(cls, name, value):
        """
        Státuszérték beállítása
        @param  name:       Státusz információ értékének a  neve
        @type   name:       C{string}
        @param  name:       Státusz információ értéke
        @type   name:       C{any}
        """
        cls.__status[name] = value


    def getStatus(cls, name):
        """
        Státuszinformáció lekérdezése

        @param  name:       Státusz információ értékének a  neve
        @type   name:       C{string}

        @return:            A névhez tartozó érték
        @rtype:             C{any}
        """
        if not name in cls.__status:
            return None
        return cls.__status[name]


    @classmethod
    def hasStatus(cls, name):
        """
        Létezik-e az adott státuszinformáció?

        @param  name:       Státusz információ értékének a  neve
        @type   name:       C{string}

        @return:            C{True} ha létezik, C{False} ha nem létezik a bejegyzés
        @rtype:             C{bool}
        """
        return name in cls.__status
