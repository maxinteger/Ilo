# -*- coding: utf -*-

__author__="Vadasz Laszlo"
__date__ ="2009.10.25. 15:56:30"

import os.path

from struct import *

from ilo.tools.strtool import fullstrip
from ilo.messages.exceptios import IloError
from ilo.structs.modelfile import ModelFile
from numpy import array as Vector
from numpy import matrix as Matrix

from ilo.tools.ooptools import *

class Q3BSP(Object):

    (Entities,              #Játékkal kapcsolatos leíró objektmok
    Textures,               #Felület leírók
    Planes,                 #Síkok a pályageometriához
    Nodes,                  #BSP fa csomópontok
    Leafs,                  #BSP fa levelek
    Leaffaces,              #Face index lista, 1/levél
    Leafbrushes,            #Brush index lista, 1/levél
    Models,                 #Merevtest geometriák a pályán
    Brushes,                #Konvex sokszög a pálya leírásaára
    Brushsides,             #Brush felület
    Vertexes,               #Verex lista a Face-ekhez
    Meshverts,              #Eltolási lista, 1/mesh
    Effects,                #Speciáliseffekt lista
    Faces,                  #Felület geometria
    Lightmaps,              #Csomagolt lightmap adatok
    Lightvols,              #helyi illumination adatok
    Visdata) = xrange(17)   #Láthatósági adatok

    def __init__(self):
        self.__data = {}

    @publicmethod
    def glInit__(self):
        pass

    @publicmethod
    def load (self, fileName):
        """
            Quake 3 BSP fájl feldogozás
        """

        def readStruct(s, offset = None):
            if offset != None:
                file_in.seek(offset)
            return s.unpack(file_in.read(s.size))

        def iterStruct(name, s):
            for i in xrange(dir[name][0], dir[name][1]+dir[name][0], s.size):
                yield readStruct(s,  i)

        sHeader         = Struct("<4si")
        sDirentry       = Struct("<ii")
        sTexture        = Struct("<64sii")
        sPlane          = Struct("<f3f")
        sNode           = Struct("<iiiiiiiii")
        sLeaf           = Struct("<iiiiiiiiiiii")
        sLeafface       = Struct("<i")
        sLeafbrush      = Struct("<i")
        sModel          = Struct("<ffffffiiii")
        sBrush          = Struct("<iii")
        sBrushsid       = Struct("<ii")
        sVertex         = Struct("<ffffffffffBBBB")
        sMeshvert       = Struct("<i")
        sEffect         = Struct("<64sii")
        sFace           = Struct("<iiiiiiiiiiiiffffffffffffii")
        sLightmap       = Struct("<49152s")                                         #128*128*3()RGB
        sLightvol       = Struct("BBBBBBBB")
        sVisdata        = Struct("ii")                                             #TODO n_vecs*sz_vecs

        dir, textures, planes, nodes, leafs, leafFaces, leafBrushes,\
        models, brushes, brushsides, vertexes, meshverts, effects, faces,\
        lightmaps, lightvols, visdata = \
        [],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]
        # @type

        geometris = []
        try:
            if os.path.exists(fileName) and os.path.isfile(fileName):
                file_in = open(fileName, "rb", 0)
            else:
                raise IOError("A fájl nem található: "+fileName)

            try:
    # ADATOK BEOLVASÁSA ########################################################

        #>-[ Fejléc ]-----------------------------------------------------------
                _, self.__data["version"] = readStruct(sHeader)
                for i in xrange(17):
                    dir.append(readStruct(sDirentry))

        #>-[ Texture ]----------------------------------------------------------
                for item in iterStruct(Q3BSP.Textures, sTexture):
                    tex, flag, cont = item
                    textures.append({"src" :tex.rstrip('\0'),                       #Név - textúra elérési útvonal
                                     "flag":flag,                                   #Flag - jelzők
                                     "cont":cont})                                  #Tartalom

        #>-[ Plane ]------------------------------------------------------------
                for item in iterStruct(Q3BSP.Planes, sPlane):
                    a1,a2, a3, b = item
                    planes.append({"norm": [a1,a2,a3],                              #Plane normál
                                   "dist": b})                                      #Távolság az origótol

        #>-[ Nodes ]------------------------------------------------------------
                for item in iterStruct(Q3BSP.Nodes, sNode):
                    a, b1,b2, c1,c2,c3, d1,d2,d3 = item
                    nodes.append({"plane":a,                                        #Plane index
                                  "child":[b1,b2],                                  #Gyerekek: pozitaív: node; negatív: leaf = -(leaf+1)
                                  "minbb":[c1,c2,c3],                               #Min Bounding Box
                                  "maxbb":[d1,d2,d3]})                              #Max Bounding Box

        #>-[ Leaf ]-------------------------------------------------------------
                for item in iterStruct(Q3BSP.Leafs, sLeaf):
                    a, b, c1,c2,c3, d1,d2,d3, e, f, g, h = item
                    leafs.append({"clast" :a,                                       #Visdata cluster index.
                                  "area"  :b,                                       #Areaportal area.
                                  "minbb" :[c1,c2,c3],                              #Integer bounding box min coord.
                                  "maxbb" :[d1,d2,d3],                              #Integer bounding box max coord.
                                  "leaff" :e,                                       #First leafface for leaf.
                                  "leaffn":f,                                       #Number of leaffaces for leaf.
                                  "leafb" :g,                                       #First leafbrush for leaf.
                                  "leafbn":h})                                      #Number of leafbrushes for leaf.

        #>-[ LeafFace ]---------------------------------------------------------
                for item in iterStruct(Q3BSP.Leaffaces, sLeafface):
                    leafFaces.append(*item)

        #>-[ LeafFace ]---------------------------------------------------------
                for item in iterStruct(Q3BSP.Leafbrushes, sLeafbrush):
                    leafBrushes.append(*item)

        #>-[ Model ]------------------------------------------------------------
                for item in iterStruct(Q3BSP.Models, sModel):
                    a1,a2,a3, b1,b2,b3, c, d, e, f = item
                    models.append({"minbb":[a1,a2,a3],
                                   "maxbb":[b1,b2,b3],
                                   "facef":c,
                                   "facen":d,
                                   "brushf":e,
                                   "brushn":f})
                                   
        #>-[ Brushes ]----------------------------------------------------------
                for item in iterStruct(Q3BSP.Brushes , sBrush):
                    a, b, c = item
                    brushes.append({"first":a,
                                    "numof":b,
                                    "texti":c})
        
        #>-[ Brushsides ]-------------------------------------------------------
                for item in iterStruct(Q3BSP.Brushsides, sBrushsid):
                    a, b = item
                    brushsides.append({"plane":a,
                                       "texti":c})
                                       
        #>-[ Vertexes ]---------------------------------------------------------
                for item in iterStruct(Q3BSP.Vertexes, sVertex):
                    a1,a2,a3, b1,b2,b3,b4, c1,c2,c3, d1,d2,d3,d4 = item
                    vertexes.append({"pos"  :[a1,a2,a3],
                                     "texc" :[[b1,b2],[b3,b4]],
                                     "norm" :[c1,c2,c3],
                                     "color":[d1,d2,d3,d4]})

        #>-[ Meshverts ]--------------------------------------------------------
                for item in iterStruct(Q3BSP.Meshverts, sMeshvert):
                    meshverts.append(*item)

        #>-[ Effects ]----------------------------------------------------------
                for item in iterStruct(Q3BSP.Effects , sEffect):
                    a, b, c = item
                    effects.append({"src"  :a,
                                    "brush":b,
                                    "unkw" :c})

        #>-[ Faces ]------------------------------------------------------------
                for item in iterStruct(Q3BSP.Faces, sFace):
                    a, b, c, d, e, f, g, h, i1,i2, j1,j2, k1,k2,k3, \
                    l1,l2,l3,l4,l5,l6, m1,m2,m3, n1,n2 = item
                    faces.append({"texti" :a,
                                  "effi"  :b,
                                  "type"  :c,
                                  "vertf" :d,
                                  "vertn" :e,
                                  "meshf" :f,
                                  "meshn" :g,
                                  "lmapi" :h,
                                  "lmstr" :[i1, i2],
                                  "lmsize":[j1, j2],
                                  "lmorig":[k1,k2,k3],
                                  "lmvecs":[[l1,l2,l3],[l4,l5,l6]],
                                  "norm"  :[m1,m2,m3],
                                  "size"  :[n1,n2]})

        #>-[ Lightmaps ]--------------------------------------------------------
                for item in iterStruct(Q3BSP.Lightmaps, sLightmap):
                    lightmaps.append(item)

        #>-[ Lightvols ]--------------------------------------------------------
                for item in iterStruct(Q3BSP.Lightvols , sLightvol):
                    a1,a2,a3, b1,b2,b3, c1,c2 = item
                    lightvols.append({"ambient"    :[a1,a2,a3],
                                      "directional":[b1,b2,b3],
                                      "dir"        :[c1,c2]})
        
        #>-[ Visdata  ]---------------------------------------------------------
#                for item in iterStruct(Q3BSP.Visdata  , sVisdata ):
#                    a, b = item
#                    data = readStruct(Struct("<B"+str(a*b)))
#                    visdata.append({"nvecs":a,
#                                     "svecs":b,
#                                     "dir"  :data})

                #print faces

            except IOError as e:
                raise IloError("Q3 BSP fájl (",fileName,") olvasási hiba:" + e)
            finally:
                file_in.close()

            for geom in geometris :
                geom.convert()

            return geometris

        except IOError:
            raise IloError("ASE fájl megnyitási hiba" + fileName)