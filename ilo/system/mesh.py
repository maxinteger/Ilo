# -*- coding: utf -*-

__author__="Vadasz Laszlo"
__date__ ="2010.01.09. 14:13:51"

from OpenGL.GL import *
from OpenGL.raw.GL.VERSION.GL_3_0 import *

import numpy

from ilo.structs.d3d import *

"""
Modell leképező modul
"""

class Mesh(object):
    """
    3D-s modell sturktúra

    Tárolja a csúcspont, lap, és él adatokat.
    A csúcs paramétereket:
     - koordináta
     - textúra koordináta
     - normál vektor
    külön C{Vertex buffer object}-ekben vannak tárolva.

    A model leképezés is itt megy végbe
    """

    __slots__ = ('__vertexes', '__vertexesUV', '__faces', '__edges',
                 '__vbo_vertex', '__vbo_normal', '__vbo_texture',
                 '__hasTexture', '__normalList', 
                 'boundingBox', 'boundingSphere',
                 'numOfVertex', 'numOfFace')

    def __init__(self, data):
        """
        Mesh inicilaizálása

        @param  data:   Mesh adatok
        @type   data:   C{ModelFile}
        """
        self.numOfVertex = data.numOfVertex                                     #:@ivar: Csúcspontok száma
        self.numOfFace   = data.numOfFace                                       #:@ivar: Háromszöglapok száma

        self.__vertexes    = []                                                 #:@ivar: Csúcs koordináták és normálvektorok listája
        self.__vertexesUV  = []                                                 #:@ivar: A csúcsok textúra koordinátáinak listája
        self.__faces       = []                                                 #:@ivar: Háromszöglapok csúcsainak a listája
        self.__edges       = []                                                 #:@ivar: Csúcsoka összekötő élek listálya

        #VertexBufferObject változók
        self.__vbo_vertex  = None                                               #:@ivar: Csúcs koordináták Vertex Buffer Objektum-a
        self.__vbo_normal  = None                                               #:@ivar: Csúcs normál vektorok Vertex Buffer Objektum-a
        self.__vbo_texture = None                                               #:@ivar: Csúcs textúra koordinátái Vertex Buffer Objektum-a

        self.__hasTexture  = data.hasVertexUV                                   #:@ivar: Vannak-e textúra koordinátái a modelnek
        self.__normalList  = None                                               #:@ivar: Csúcs normálvektorok GLlistája a vektorok megjelenítéséhez

        for i in xrange(len(data.vertex)):
            self.__vertexes.append(Vertex(data.vertex[i], data.vertexNormal[i], i))

        if data.hasVertexUV:
            for i in xrange(len(data.vertexUV)):
                self.__vertexesUV.append(VertexUV(data.vertexUV[i], i))

        for i in xrange(len(data.face)):
            fv = data.getFaceByIndex(i)
            for j in xrange(3):
                self.__vertexes[fv[j]].norm = data.getVertexNormalByIndex(fv[j])

        for face in data.face:
            for i in face:
                self.__vertexes[i].norm = data.getVertexNormalByIndex(i)

        for i in xrange(len(data.face)):
            v  = [self.__vertexes[x] for x in data.face[i]]
            uv = [self.__vertexesUV[x] for x in data.faceUV[i]]
            f  = data.faceNormal[i]
            self.__faces.append(Face(v, uv, f, i))

        edge = {}
        for face in self.__faces:
            last = face.verts[-1]
            for v in face.verts:
                if not (((v, last) in edge) or ((last, v) in edge)):
                    edge[(v,last)] = [face.index]
                else:
#                    edge[(last,v)].append(face.index)
                    pass
                last = v


        for key, e in edge.iteritems():
            self.__edges.append(Edge(key[0], key[1], e[0], e[-1]))

        self.boundingBox    = BoundBox(self.__vertexes)                         #:@ivar: Befoglaló doboz
        self.boundingSphere = BoundShpere(self.__vertexes)                      #:@ivar: Befoglaló gömb
        
        self.__createBuffers()


    def __createBuffers(self):
        """
        Csúcs koordináták, normál vektor és textúra koordináták kiszámítása és a
        Vertex Buffer Object-ek inicilaizálása
        """

        vertex, normal, uv = [], [], []

        for face in self.__faces :
            for v in face.verts:
                vertex.append(v.vert)
                normal.append(v.norm)
            if self.__hasTexture :
                for u in face.uvs:
                    uv.append(u.uv)

        vertex = numpy.array(vertex , numpy.float32)
        normal = numpy.array(normal , numpy.float32)
        uv     = numpy.array(uv     , numpy.float32)

        self.__vbo_vertex = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.__vbo_vertex)
        glBufferData(GL_ARRAY_BUFFER, vertex, GL_STATIC_DRAW)

        self.__vbo_normal = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.__vbo_normal)
        glBufferData(GL_ARRAY_BUFFER, normal, GL_STATIC_DRAW)

        self.__vbo_texture = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.__vbo_texture)
        glBufferData(GL_ARRAY_BUFFER, uv, GL_STATIC_DRAW)


    def renderMesh (self, frontFaces=[]):
        """
        Vertex Object Buffer-ek leképezése

        @param  frontFaces: A látható lapok listája
        @type   frontFaces: C{list}
        """

        glBindBuffer(GL_ARRAY_BUFFER, self.__vbo_vertex)
        glVertexPointer(3, GL_FLOAT, 0, None)

        glBindBuffer(GL_ARRAY_BUFFER, self.__vbo_normal)
        glNormalPointer(GL_FLOAT, 0, None)

        glBindBuffer(GL_ARRAY_BUFFER, self.__vbo_texture)
        glTexCoordPointer(2, GL_FLOAT, 0, None)

        glDrawArrays(GL_TRIANGLES, 0, self.numOfFace * 3)
        #glDrawElements(GL_TRIANGLES, len(frontFaces), GL_UNSIGNED_INT, frontFaces)


    def renderNormalVectors(self):
        """
        Vertex normál vektorok megjelenítése C{glList} segítségével
        """
        if self.__normalList:
            glCallList(self.__normalList)


    def showNormalVectors(self):
        """
        A csúcs normálvektorainak megjelenítéséhez szükséges C{glList}
        létrehozása és számított adatokkal (csúcspont koordináták + eltolás)
        való feltöltés.
        """
        self.__normalList = glGenLists(1)
        glNewList(self.__normalList, GL_COMPILE)
        glBegin(GL_LINES)
        glColor(1.,1.,1.)
        def add(x, y): return x + y
        #vertex normal
        for i in self.__vertexes:
            glVertex3fv(i.vert)
            glVertex3fv(i.vert+i.norm*3)
        #face normal
        glColor(1.,0.,1.)
        for i in self.__faces:
            center = (i.verts[0].vert + i.verts[1].vert + i.verts[2].vert) / 3.0
            glVertex3fv(center)
            glVertex3fv(i.norm *10 + center)
        glEnd()
        glEndList()


    def hideNormalVectors(self):
        """
        Csúcs normálvektorok megjelenítési listájának (C{glList}) törlése
        """
        if self.__normalList:
            glDeleteLists(self.__normalList, 1)
            self.__normalList = None


    def remove(self):
        """
        Geometria adatok törlése
        """
        self.hideNormalVectors()
        glDeleteBuffers([self.__vbo_normal,
                         self.__vbo_texture,
                         self.__vbo_vertex])

    @property
    def vertexes(self):
        """Csúcspontok listája"""
        return self.__vertexes

    @property
    def faces(self):
        """Lapok listája"""
        return self.__faces

    @property
    def edges(self):
        """Élek listája"""
        return self.__edges

