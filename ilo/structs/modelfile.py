# -*- coding: utf -*-

__author__="Vadasz Laszlo"
__date__ ="2009.10.01. 19:12:32"

import numpy

class ModelFile:

    __slots__ = ('__model',)

    def __init__(self):
        self.__model = {}
        self.__model["name"] = ""
        for key in ["numVertex",
                    "numFace",
                    "numColorVertex",
                    "numColorFace",
                    "numTexVertex",
                    "numTexFace"]:
            self.__model[key] = 0
        for key in ["listVertex",
                    "listFace",
                    "listEdge",
                    "listColorVertex",
                    "listColorFace",
                    "listTexVertex",
                    "listTexFace",
                    "listVertexNormal",
                    "listFaceNormal"]:
            self.__model[key] = []

    def convert(self):
        for key, item in self.__model.iteritems() :
            if key in ["listVertex", "listColorVertex", "listTexVertex", "listVertexNormal", "listFaceNormal"]:
                self.__model[key] = numpy.array(item, dtype=numpy.float32)
            elif key in ["listFace", "listColorFace", "listTexFace"] :
                self.__model[key] = numpy.array(item, dtype=numpy.int16)

    @property
    def numOfVertex(self):
        return len(self.__model["listVertex"])

    @property
    def numOfFace(self):
        return len(self.__model["listFace"])

    @property
    def hasVertexNormal(self):
        return len(self.__model["listVertexNormal"]) > 0

    @property
    def hasVertexUV(self):
        return len(self.__model["listTexVertex"]) > 0

    @property
    def hasVertexColor(self):
        return len(self.__model["listColorVertex"]) > 0

#Getter / Setter

    @property
    def name(self):
        return self.__model["name"]

    @name.setter
    def name(self, value):
        self.__model["name"] = value

    #Vertex-------------------------------------------
    @property
    def vertex(self):
        if len(self.__model["listVertex"]) > 0:
            return self.__model["listVertex"]
        return None

    @vertex.setter
    def vertex (self, value):
        self.__model["listVertex"] = value
    
    def addVertex(self, value):
        self.__model["listVertex"].append(value)

    def getVertexByIndex(self, index):
        if self.vertex != None:
            return self.vertex[index]
        return None

    #Vertex Normal-------------------------------------------
    @property
    def vertexNormal(self):
        if len(self.__model["listVertexNormal"]) > 0:
            return self.__model["listVertexNormal"]
        return None

    @vertexNormal.setter
    def vertexNormal (self, value):
        self.__model["listVertexNormal"] = value

    def addVertexNormal(self, value):
        self.__model["listVertexNormal"].append(value)

    def getVertexNormalByIndex(self, index):
        if self.vertexNormal != None:
            return self.vertexNormal[index]
        return None

    #Vertex UV -------------------------------------------
    @property
    def vertexUV(self):
        if len(self.__model["listTexVertex"]) > 0:
            return self.__model["listTexVertex"]
        return None

    @vertexUV.setter
    def vertexUV (self, value):
        self.__model["listTexVertex"] = value

    def addVertexUV(self, value):
        self.__model["listTexVertex"].append(value)

    def getVertexUVByIndex(self, index):
        if self.vertexUV != None:
            return self.vertexUV[index]
        return None


    #Vertex Color-------------------------------------------
    @property
    def vertexColor(self):
        if len(self.__model["listColorVertex"]) > 0:
            return self.__model["listColorVertex"]
        return None

    @vertexColor.setter
    def vertexColor (self, value):
        self.__model["listColorVertex"] = value

    def addVertexColor(self, value):
        self.__model["listColorVertex"].append(value)

    def getVertexColorByIndex(self, index):
        if self.vertexColor != None:
            return self.vertexColor[index]
        return None

    #Face-------------------------------------------
    @property
    def face(self):
        if len(self.__model["listFace"]) > 0:
            return self.__model["listFace"]
        return None

    @face.setter
    def face (self, value):
        self.__model["listFace"] = value

    def addFace(self, value):
        self.__model["listFace"].append(value)

    def getFaceByIndex(self, index):
        if self.face != None:
            return self.face[index]
        return None

    #Face Normal -------------------------------------------
    @property
    def faceNormal(self):
        if len(self.__model["listFaceNormal"]) > 0:
            return self.__model["listFaceNormal"]
        return None

    @faceNormal.setter
    def faceNormal (self, value):
        self.__model["listFaceNormal"] = value

    def addFaceNormal(self, value):
        self.__model["listFaceNormal"].append(value)

    def getFaceNormalByIndex(self, index):
        if self.faceNormal != None:
            return self.faceNormal[index]
        return None

    #Face UV -------------------------------------------
    @property
    def faceUV(self):
        if len(self.__model["listTexFace"]) > 0:
            return self.__model["listTexFace"]
        return None

    @faceUV.setter
    def faceUV (self, value):
        self.__model["listTexFace"] = value

    def addFaceUV(self, value):
        self.__model["listTexFace"].append(value)

    def getFaceUVByIndex(self, index):
        if self.faceUV != None:
            return self.faceUV[index]
        return None

    #Face Color -------------------------------------------
    @property
    def faceColor(self):
        if len(self.__model["listColorFace"]) > 0:
            return self.__model["listColorFace"]
        return None

    @faceColor.setter
    def faceColor (self, value):
        self.__model["listColorFace"] = value

    def addFaceColor(self, value):
        self.__model["listColorFace"].append(value)

    def getFaceColorByIndex(self, index):
        if self.faceColor != None:
            return self.faceColor[index]
        return  None

    #Edge-------------------------------------------------------
    @property
    def edge(self):
        if len(self.__model["edge"]) > 0:
            return self.__model["edge"]
        return None

    @edge.setter
    def edge(self, value):
        self.__model["edge"] = value

    def addEdge(self, value):
        self.__model["edge"].append(value)

    def getEdgeByIndex(self, index):
        if self.edge != None:
            return self.edge[index]
        return None

