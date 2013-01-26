# -*- coding: utf -*-

__author__="Vadasz Laszlo"
__date__ = "2009.07.21. 21:46:18"

from ilo.messages.exceptios import *
import os.path

from ilo.tools.strtool import fullstrip
from ilo.messages.exceptios import IloError
from ilo.structs.modelfile import ModelFile


def loadASEFile (fileName):
    """
    ASE (ASCII Scene Export) fájl feldogozás
    """
    geometris = []
    try:
        if os.path.exists(fileName) and os.path.isfile(fileName):
            file_in = open(fileName, "r", 0)
        else:
            raise IOError("A fajl nem talalhato: %s" % fileName)

        try:
            for line in file_in:
                line = fullstrip(line, True)
                if len(line) > 0:
                    if "*COMMENT" in line[0]:
                        #print " ".join (line[1:]).split('"')                                                           #COMMENT
                        pass
                    if "*SCANE" in line[0]:                                                                            #SCENE
                        #TODO ASE scane információk feldolgozása
                        pass
                    if "*GEOMOBJECT" in line[0]:                                                                       #GEOMOBJECT
                        #initgeometry
                        geometry = ModelFile()
                        for geomLine in file_in:
                            geomLine = fullstrip(geomLine, True)
                            if "*NODE_NAME" in geomLine[0]:
                                geometry.name = geomLine[1].split('"')[1]
                            elif "*NODE_TM" in geomLine[0]:                                                            #NODE
                                #TODO parse ASE node information
                                for nodeLine in file_in:
                                    nodeLine = fullstrip(nodeLine, True)
                                    if nodeLine[0] == '}':
                                        break
                            elif "*MESH" in geomLine[0]:
                                for meshLine in file_in:
                                    meshLine = fullstrip(meshLine, True)
                                    if "*TIMEVALUE" in meshLine[0]:
                                        #TODO parse ASE timevalue
                                        pass
                                    elif "*MESH_NUMVERTEX" in meshLine[0]:                                             #VERTEX
                                        pass    #számítható paraméter!
                                    elif "*MESH_VERTEX_LIST" in meshLine[0]:
                                        for vertLine in file_in:
                                            vertLine = fullstrip(vertLine, True)
                                            if "*MESH_VERTEX" in vertLine[0]:
                                                geometry.addVertex([float(n) for n in vertLine[2:5]])
                                            else:
                                                break
                                    elif "*MESH_NUMFACES" in meshLine[0]:                                              #FACE
                                        pass    #számítható paraméter!
                                    elif "*MESH_FACE_LIST" in meshLine[0]:
                                        for faceLine in file_in:
                                            faceLine = fullstrip(faceLine, True)
                                            if "*MESH_FACE" in faceLine[0]:
                                                #TODO face adatok feldolgozása
                                                #flag = {}#{"edge":edge, "smooth":faceLine[15], "matid":faceLine[17]}
                                                vertList = [int(faceLine[i]) for i in [3, 5, 7]]
                                                geometry.addFace(vertList)
                                                #geometry["listFlag"].append(flag)
                                            else:
                                                break
                                    elif "*MESH_NUMCVERTEX" in meshLine[0]:                                            #ColorVERTEX
                                        pass    #számítható paraméter!
                                    elif "MESH_CVERTLIST" in meshLine[0]:
                                        for cvertLine in file_in:
                                            cvertLine = fullstrip(cvertLine, True)
                                            if "MESH_VERTCOL" in cvertLine[0]:
                                                geometry.addVertexColor([float(n) for n in cvertLine[2:5]])
                                            else:
                                                break
                                    elif "*MESH_NUMCVFACES" in meshLine[0]:                                            #ColorFACE
                                        pass    #számítható paraméter!
                                    elif "*MESH_CFACELIST" in meshLine[0]:
                                        for cfaceLine in file_in:
                                            cfaceLine = fullstrip(cfaceLine, True)
                                            if "*MESH_CFACE" in cfaceLine[0]:
                                                geometry.addFaceColor([int(n) for n in cfaceLine[2:5]])
                                            else:
                                                break
                                    elif "*MESH_NUMTVERTEX" in meshLine[0]:                                            #TextureVERTEX
                                        pass    #számítható paraméter!
                                    elif "MESH_TVERTLIST" in meshLine[0]:
                                        for tvertLine in file_in:
                                            tvertLine = fullstrip(tvertLine, True)
                                            if "MESH_TVERT" in tvertLine[0]:
                                                geometry.addVertexUV([float(n) for n in tvertLine[2:4]])
                                            else:
                                                break
                                    elif "*MESH_NUMTVFACES" in meshLine[0]:                                            #TextureFACE
                                        pass    #számítható paraméter!
                                    elif "*MESH_TFACELIST" in meshLine[0]:
                                        for tfaceLine in file_in:
                                            tfaceLine = fullstrip(tfaceLine, True)
                                            if "*MESH_TFACE" in tfaceLine[0]:
                                                geometry.addFaceUV([int(n) for n in tfaceLine[2:5]])
                                            else:
                                                break
                                    elif "*MESH_NORMALS" in meshLine[0]:                                               #NORMALS
                                        vnormals = {}
                                        for normLine in file_in:
                                            normLine = fullstrip(normLine, True)
                                            if "*MESH_VERTEXNORMAL" in normLine[0]:
                                                vnormals[int(normLine[1])] = [float(n) for n in normLine[2:5]]
                                            elif "*MESH_FACENORMAL" in normLine[0]:
                                                geometry.addFaceNormal([float(n) for n in normLine[2:5]])
                                            else:
                                                break
                                        for i in xrange(len(vnormals.values())):
                                            geometry.addVertexNormal(vnormals[i])
                                    elif meshLine[0] == '}':
                                        break
                            elif "*PROP_MOTIONBLUR" in line[0]:
                                pass
                            elif "*PROP_CASTSHADOW" in line[0]:
                                pass
                            elif "*PROP_RECVSHADOW" in line[0]:
                                pass
                            elif "*MATERIAL_REF" in line[0]:
                                pass
                            elif geomLine[0] == '}' :
                                break
                        geometris.append(geometry)

        except IOError as e:
            raise IloError("ASE fajl (:", fileName, ") olvasasi hiba:" + e)
        finally:
            file_in.close()

        for geom in geometris :
            geom.convert()

        print "File is loaded %s" % (fileName)
        return geometris

    except IOError:
        raise IloError("ASE fajl megnyitasi hiba %s" % fileName)
        

if __name__ == "__main__":
    ase = load("/home/max/texture.ase")
