# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="max"
__date__ ="$2009.10.29. 13:50:50$"

from ilo.tools.ilomath import *
from OpenGL.GL import *
from OpenGL.raw.GL.VERSION.GL_3_0 import *

from ilo.config import *
from ilo.messages.exceptios import IloError
from ilo.structs.vector import *


def drawShadowVolume(geom, renderObj, light ):
    glPushMatrix()
    #glLoadIdentity()
    light = light[0].link
    coord = Vector3([-100.0,-50.0,100.0])


    #light.coord = light.coord + renderObj.coord* renderObj.scale
    glBegin(GL_POINTS)
    glColor(1.,1.,0.)
    glVertex(coord)

    glColor(1.,1.,1.)
    glVertex(coord *10)
    glEnd()

    

    if False:
        # extrude vertices

        # NOTE that for directional lights all vertices will be extruded
        # to the same point, so in that case you do not need to
        # calculate this array.  We do not implement this optimization.
        def directionToPoint(light, vertex):
            if light.isDirectionalLight:
                return Vector3(coord) * -1
            else:
                return (vertex.vert - Vector3(coord))


        def extrudVertex(item):
            return directionToPoint(light, item)

        def backFace(item):
            #print item.norm,  extrudedVertex[item.verts[0].index], item.norm * extrudedVertex[item.verts[0].index]
            return ((item.norm * extrudedVertex[item.verts[0].index]) > 0).any()
        
        def getEdge(item):
            return isBackface[item.faces[0]] ^ isBackface[item.faces[1]]

        extrudedVertex = map(extrudVertex, geom.vertexes)
        isBackface = map(backFace,geom.faces)
        silhouetteEdge = filter(getEdge, geom.edges)

        #print "---------------------------------------"

        for x in extrudedVertex:
            glBegin(GL_LINES)
            glColor(0.0, 1.0,0.0)
            glVertex(coord)
            glVertex(coord + x)
            glEnd()


    #geom.extrusionDirty = False

    if False:
        # find silhouette edges and extrude them into faces
        glBegin(GL_LINES)
        for edge in silhouetteEdge:
            reg0 = (edge.verts[0].vert.tolist() + [1.0])
            reg1 = (edge.verts[1].vert.tolist() + [1.0])
            ext0 = (edge.verts[0].vert.tolist() + [0.0])
            ext1 = (edge.verts[1].vert.tolist() + [0.0])

            glColor(1.,1.,0.)
            glVertex(edge.verts[0].vert)
            glVertex(edge.verts[1].vert)

#            if isBackface[edge.faces[0]]:
#                glColor(1.0, 0.0,0.0)
#                glVertex(reg0)
#                glVertex(ext1)
#                glVertex(reg1)
#                glVertex(ext0)
#            else:
#                glColor(0.0,1.0,1.0)
#                glVertex(reg1)
#                glVertex(ext0)
#                glVertex(reg0)
#                glVertex(ext1)
        glEnd()
    glPopMatrix()
        # draw front cap
#        if frontCap:
#            glBegin(GL_TRIANGLES)
#            for i in xrange(len(geom.__face)):
#                if not isBackface[i]:
#                    for j in xrange(3):
#                        glVertex(geom.__vertex[geom.__face[i][j]])
#                    polyCount += 1
#            glEnd()
#
#        useBackCapOptimization = False
#
#        if light.isDirectionalLight:
#            # we can actually skip the back cap entirely
#            # in this case
#            useBackCapOptimization = True
#        else:
#            # if we have a point light and we are doing shadow
#            # optimizations then we can use the fan optimization
#            # if the point light is outside of the bounding sphere
#            # of the model, (the OpenGL specifications do not require
#            # correct rendering of triangles at inifinity that span
#            # larger then 180 degrees)
#            lightPos = Vector3(light.coord[0:3])
#
#            # light and lightPos are in object space
#            useBackCapOptimization = ((lightPos - geom.boundingSphere.center).length() > geom.boundingSphere.radius)

        # draw back cap
        # if we are using a directional light the end cap
        # will be infinitely small and we don't have to draw it
#        if endCap and not light.isDirectionalLight:
#            # draw back cap
#            if useBackCapOptimization:
#                # optimized triangle fan for back cap
#                firstPoint = extrudedVertex[geom.__edge[0].vertex[0]] + [0]
#                glBegin(GL_TRIANGLES)
#                for edge in silhouetteEdge:
#                    vIndex0 = edge.vertex[0]
#                    vIndex1 = edge.vertex[1]
#                    glVertex(firstPoint)
#                    if isBackface[edge.face[0]]:
#                        glVertex(extrudedVertex[vIndex0] + [0])
#                        glVertex(extrudedVertex[vIndex1] + [0])
#                    else:
#                        glVertex(extrudedVertex[vIndex1] + [0])
#                        glVertex(extrudedVertex[vIndex0] + [0])
#                    polyCount += 1
#                glEnd()
#            else:
#                # unoptimized back faces for back cap
#                glBegin(GL_TRIANGLES)
#                for i in xrange(len(geom.__face)):
#                    if isBackface[i]:
#                        for j in xrange(3):
#                            glVertex(geom.__vertex[geom.__face[i][j]] + [0])
#                        polyCount += 1
#                glEnd()