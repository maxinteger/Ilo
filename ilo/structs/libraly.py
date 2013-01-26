# -*- coding: utf -*-

__author__="Vadasz Laszlo"
__date__ ="2010.02.23. 7:14:16"


import os.path
from xml.dom.minidom import *

from ilo.system.mesh import Mesh
from ilo.system.material import *
from ilo.render.display import *
from ilo.structs.vector import *
from ilo.messages.exceptios import *
from ilo.filereader.model.ase import loadASEFile

"""
A grefikai erőforrás kezeléssel foglalkozó osztályokat tartalamzó modul
"""

class Libraly (object):
    """
    Grafikai erőforrás kezelő

    Egységesen kezeli a textúra és geometria adatokat.
    A struktúrában tárolt adatok könnyen újrahasznosíthatóvá és elérhetővé
    teszi a már betöltött objektumoat.
    Elemeket adhatunk és törölhetünk a megfelelő metódushívásokkal,
    a felvett adatokra egyedi névvel hívatkozhatunk

    Az adatokat külső xml alapú adatfájlokból is betölthetjük a megfelelő
    metódus hívás segítségével
    """

    __slots__ = ('__geometryLib', '__materialLib')

    _instance = None                                                            #:@cvar: Az osztály egyetelen példánya

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Libraly, cls).__new__( cls, *args, **kwargs)
            return cls._instance
        else:
            raise SingletonClassError("Csak egyszer példányosítható!")

    def __init__(self):
        """
        Az adattároló listák inicializálása
        """
        self.__geometryLib = {}                                                 #:@ivar: Geometria tároló
        self.__materialLib = {}                                                 #:@ivar: Material tároló

    @classmethod
    def getInstance(cls):
        """
        Az osztály egyetlen létező példányát adja vissza

        return: Osztály példány
        rtype:  C{Libraly}
        """
        return cls._instance

#{ Geometriák
    def getGeometry(self, id):
        """
        A tárolóban lévő geometria lekérdezése.
        Ha a geometria azoosítója (C{id}) nem létezik, akkor kivétel keletkezik.

        @param  id:     A geometria egyedi azonosítója a tárolóban
        @type   id:     C{String}

        @return:        A megadott azonosítóval jelölt geometria
        @rtype:         C{Mesh}
        """
        if id in self.__geometryLib:
            return self.__geometryLib[id]
        else:
            raise IloLibralyErro("Nem letezo geometria azonosito: %s" % id)


    def addGeometry(self, id, data):
        """
        Új geometria hozzáadása a tárolóhoz.
        Ha a geometria azoosítója (C{id}) már létezik, akkor kivétel keletkezik.

        @param  id:     A geometria egyedi azonosítója a tárolóban
        @type   id:     C{String}
        @param  data:   Geometria példány
        @type   data:   C{Material}

        @return:        A felvett geometria, láncolás céljából
        @rtype:         C{Material}
        """
        if id not in self.__materialLib :
            self.__geometryLib[id] = data
            return data
        else:
            raise IloLibralyErro("Letezo geometria azonosito: %s" % id)


    def removeGeometry(self, id):
        """
        Az azonosítóval (C{id}) megadott geometria dörlése a tárolóból
        Nemlétező azonosító esetén kivétel keletkezik

        @param  id:     A geometria egydi azonosítója a tárolóban
        @type   id:     C{String}
        """
        if id in self.__geometryLib:
            self.__geometryLib[id].remove()
            del self.__geometryLib[id]
        else:
            raise IloLibralyErro("Nem létező geometria azonosító: %s" % id)


    def removeAllGeometris(self):
        """
        Törli az összes geometriát a tárolóból
        """
        for geom in self.__geometryLib.values():
            geom.remove()
        self.__geometryLib = {}


    def hasGeometry(self, id):
        """
        Ellenőrizzük a geometria azonosító létezését

        @param  id:     A geometria egyedi azonosítója a tárolóban
        @type   id:     C{String}
        @return:        Létezik-e az adott geometria, igen:C{True}; nem:C{False}
        @rtype:         C{Boolean}
        """
        return id in self.__geometryLib


    def addGeometryFromFile(self, fileName, format="ase", geomIDs=None):
        """
        Geometriák beolvasása (ASE) fájlból
        Egy geometria fájl több objektumot is tárolhat. A metódus a `geomIDs`-
        ban felsorol azonosítók alapján olvassa be az objektumokat, ha ez nincs
        meg adva, vagy a listában szerepel a '*' karakter akkor az összes
        objektumot beolvassa.
        Minden objektum a fájlban található objetumazonosítóval érhető el.

        @param  fileName:   A geometria fájl neve és elérési útvonala
        @type   fileName:   C{string}
        @param  format:     A beolvasandó geometria fájl formátuma
        @type   format:     C{string}
        @param  geomIDs:    A fálból kilvasandó modellek azonosítója
                            Az alpértelmezett C{None} esetén mindet beolvassa
        @type   geomIDs:    C{list}

        @return:            A betöltött objektmok azonosítóinak a listája
        @rtype:             C{list}
        """
        if format == "ase":
            geoms = loadASEFile(fileName)
        else:
            raise IloError("Ismeretlen fajlformatum!" + format)

        if '*' in geomIDs: geomIDs = None

        addedIDs = []

        for geom in geoms:
            if geomIDs  == None or geom.name in geomIDs:
                self.addGeometry(geom.name, Mesh(geom))
                addedIDs.append(geom.name)

        return addedIDs
#}


#{ Anyagjellemzők

    def getMaterial(self, id):
        """
        A tárolóban lévő anyagminta lekérdezése
        Ha az anyagminta azonosítója (C{id}) nem létezik akkor kivétel
        keletkezik

        @param  id:     Az anyagminta egyedi azonosítója a tárolóban
        @type   id:     C{String}

        @return:        A megadott azonosítóval jelölt anyagminta
        @rtype:         C{Material}
        """
        if id == None: return None
        if id in self.__materialLib :
            return self.__materialLib[id]
        else:
            raise IloLibralyErro("Nem letezo anyagminta azonosito: %s" % id)


    def addMaterial(self, id, data):
        """
        Új anyagminta hozzáadása a tárolóhoz
        Ha az anyagminta neve (C{id}) már létezik akkor kivétel keletkezik

        @param  id:     Az anyagminta egyedi azonosítója a tárolóban
        @type   id:     C{String}
        @param  data:   Anyagminta példány
        @type   data:   C{Material}

        @return:        A felvett anyagminta, láncolás céljából
        @rtype:         C{Material}
        """
        if id not in self.__materialLib :
            self.__materialLib[id] = data
            return data
        else:
            raise IloLibralyErro("Letezo anyagminta azonosito: %s" % id)


    def removeMaterial(self, id):
        """
        Az azonosítóval (C{id}) megadott anyagminta dörlése a tárolóból
        Nemlétező azonosító esetén kivétel keletkezik

        @param  id:     Az anyagminta egydi azonosítója a tárolóban
        @type   id:     C{String}
        """
        if id in self.__materialLib :
            self.__materialLib[id].remove()
            del self.__materialLib[id]
        else:
            raise IloLibralyErro("Nem letezo anyagminta azonosito: %s" % id)


    def removeAllMatreials(self):
        """
        Törli az összes anyagmintát a tárolóból
        """
        for material in self.__materialLib.values():
            material.remove()
        self.__materialLib = {}


    def hasMaterial(self, id):
        """
        Ellenőrizzük az anyagminte azonosító létezését

        @param  id:     Az anyagminta egyedi azonosítója a tárolóban
        @type   id:     C{String}
        @return:        Létezik-e az adott jellemző, igen:C{True}; nem:C{False}
        @rtype:         C{Boolean}
        """
        return id in self.__materialLib


    def addXIMMatlib(self, ximFile, matIDList = None):
        """
        Anyagminták betöltése XIM (Xml Ilo Matlib) fájlból

        @param  ximFile:    A XIM fájl neve és elérési útvonala
        @type   ximFile:    C{String}
        @param  matIDList:  A betöltendő anyagminták azonosítóinak listája,
                            C{None} esetben mindet betölti
                            C{default: None}
        @type   matIDList:  C{List}
        """
        if os.path.exists(ximFile) and os.path.isfile(ximFile):
            file_in = open(ximFile, "r", 0)
            xData = parse(file_in)
        else:
            raise IloError("A fajl nem talalhato: %s" % ximFile)

        for mat in xData.getElementsByTagName("material"):
            if (not bool(matIDList)) or (mat.getAttribute("id") in matIDList):
                material   = None

                matParams  = []
                matid      = mat.getAttribute("id")
                properties = mat.getElementsByTagName("properties")[0]
                texture    = mat.getElementsByTagName("texture")[0]

                for properti in ["ambient", "diffuse", "specular", "emission"]:
                    matParams.append([float(x) for x in properties.getAttribute(properti).split(";")])
                matParams.append(float(properties.getAttribute("shininess")))

                material = Material(*matParams)

                material.setTexture(Texture(
                    texture.getAttribute("src"),
                    texture.getAttribute("filter")
                ))

                try:    vertShader = mat.getElementsByTagName("vertexshader")[0].firstChild.wholeText.strip()
                except: vertShader = ""

                try:    fragShader = mat.getElementsByTagName("fragmentshader")[0].firstChild.wholeText.strip()
                except: fragShader = ""

                if (vertShader != "" and fragShader != ""):
                    material.setShader(Shader(vertShader,fragShader))

                self.addMaterial(matid, material)

        xData.unlink()

        if not material:
            raise IloError("A megadott anyagminta azonosito(k) nem talalhato(k): %s" % matIDList)
#}


    def loadSceneXML(self, xisFile):
        """
        XIS (Xml Ilo Scene) fájl beöltése

        A fájlban található geometriai és anyagjellemző adatokat közvetlenül a
        C{Libraly}-be tölti, majd a fájl által leírt struktúrának megfelelően
        összeállítja az ezzel azonos belső objektum szerkezetet
        C{RenderObjekt}-ek segítségével

        @param  xisFile:    XIS (Xml Ilo Scene) fájlneve és elrési útvonala
        @type   xisFile:    C{String}

        @return: Az összeállított struktúrát tartalmazó C{RenderObjectContainer}
        @rtype:  C{RenderObjectContainer}
        """

        if os.path.exists(xisFile) and os.path.isfile(xisFile):
            scene = {}
            try:
                file_in = open(xisFile, "r")

                xData = parse(file_in)
                #Scene adatok olvasása
                details = {}
                details["sceneid"]   = xData.getElementsByTagName("sceneid")
                details["scenename"] = xData.getElementsByTagName("scenename")
                details["scenetype"] = xData.getElementsByTagName("scenetype")

                scene["details"] = details

                #Modellek regisztrálása
                geometryLibs = {}
                for geo in xData.getElementsByTagName("geometry"):
                    name = geo.getAttribute("id")
                    geometryLibs[name] = {
                        "file"   : geo.getAttribute("src"),
                        "format" : geo.getAttribute("format"),
                        "geoIDs" : []
                    }
                    

                #Anyagminták regisztrálása
                materialLibs = {}
                for mat in xData.getElementsByTagName("matlib"):
                    name = mat.getAttribute("id")
                    materialLibs[name] = {
                        "file"   : mat.getAttribute("src"),
                        "matIDs" : []
                    }

                #Scene objektumok olvasása
                sceneObj = {}
                for obj in xData.getElementsByTagName("object"):
                    element = {}
                    for attr in ["id", "geometry", "texture", "visible", "hittest",\
                                 "shadow", "coord", "angle", "scale"]:
                        element[attr] = None
                        value = obj.getAttribute(attr)
                        if value != "":
                            if attr == "id":
                                element[attr] = value
                            elif attr == "geometry":
                                geomFile, geomID = value.split(".")
                                if geomID not in geometryLibs[geomFile]["geoIDs"]:
                                    geometryLibs[geomFile]["geoIDs"].append(geomID)
                                element[attr] = geomID
                            elif attr == "texture":
                                matLib, matID = value.split(".")
                                if (matID not in materialLibs[matLib]["matIDs"]) and (matID !=""):
                                    materialLibs[matLib]["matIDs"].append(matID)
                                element[attr] = matID
                            elif attr in ["visible", "hittest", "shadow"]:
                                element[attr] = (value == "1")
                            else:
                                element[attr] = [float(x) for x in value.split(";")]
                    sceneObj[element["id"]] = element

                #Modellek betöltése a modeltárba
                for data in geometryLibs.values():
                    self.addGeometryFromFile(data["file"], data["format"], data["geoIDs"])

                #Anyagminták betöltése az anyagtárba
                for data in materialLibs.values():
                    self.addXIMMatlib(data["file"], data["matIDs"])

                #RenderObjetc szerkezet felépítése

                def setupObject(element):
                    obj = RenderObjectContainer(element["id"],
                                               self.getGeometry(element["geometry"]),
                                               self.getMaterial(element["texture"]))
                    obj.scale  = element["scale"]
                    obj.coord  = element["coord"]
                    obj.angle  = element["angle"]

                    return obj

                sceneObject = RenderObjectContainer("alap")

                sceneObject = setupObject(sceneObj["main"])
                
                for key, item in sceneObj.iteritems():
                    if key != "main":
                        sceneObject.addElement(setupObject(item))

                return sceneObject

                file_in.close()
            except IOError as err:
                raise IloError ("A fájl %s olvasási hiba " % xisFile, err)
        else:
            raise IOError("A fájl nem található: %s" % xisFile)

    