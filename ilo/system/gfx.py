# -*- coding: utf -*-

"""
    Az OpenGL grafikus könyvtár becsomagolása mely Josh Beam Drome Engine
    projektje alapján készült
    Lásd:
    http://joshbeam.com/software/drome_engine/
"""


__author__= ("Josh Beam", "Vadasz Laszlo")
__date__ ="2010.01.09. 11:04:11"
__all__ = ["Gfx", "GLContext", "Viewport"]



import math
from OpenGL.raw.GL import *

from OpenGL.GL import *
from OpenGL.GLU import *

from ilo.config import Config
from ilo.structs.matrix import Matrix4x4
from ilo.messages.exceptios import *
from ilo.system.material import Texture
from ilo.system.text import Text

#-------------------------------------------------------------------------------

class Gfx(object):
    """
    Gfx konstans gyűjtemény
    """
    PROJECTION                  = GL_PROJECTION
    MODELVIEW                   = GL_MODELVIEW
    TEXTURE                     = GL_TEXTURE

    COLOR_BUFFER_BIT            = GL_COLOR_BUFFER_BIT
    DEPTH_BUFFER_BIT            = GL_DEPTH_BUFFER_BIT
    STENCIL_BUFFER_BIT          = GL_STENCIL_BUFFER_BIT

    TRIANGLES                   = GL_TRIANGLES
    TRISTRIP                    = GL_TRIANGLE_STRIP
    TRIFAN                      = GL_TRIANGLE_FAN
    QUADS                       = GL_QUADS
    LINES                       = GL_LINES
    POINTS                      = GL_POINTS

    TEXTURE_1D                  = GL_TEXTURE_1D
    TEXTURE_2D                  = GL_TEXTURE_2D
    TEXTURE_3D                  = GL_TEXTURE_3D

    TEXTURE_UNIT_0              = GL_TEXTURE0
    TEXTURE_UNIT_1              = GL_TEXTURE0 + 1
    TEXTURE_UNIT_2              = GL_TEXTURE0 + 2
    TEXTURE_UNIT_3              = GL_TEXTURE0 + 3
    TEXTURE_UNIT_4              = GL_TEXTURE0 + 4
    TEXTURE_UNIT_5              = GL_TEXTURE0 + 5
    TEXTURE_UNIT_6              = GL_TEXTURE0 + 6
    TEXTURE_UNIT_7              = GL_TEXTURE0 + 7
    TEXTURE_UNIT_8              = GL_TEXTURE0 + 8
    TEXTURE_UNIT_9              = GL_TEXTURE0 + 9

    NUM_TEXTURE_UNITS           = 10

    TEXTURE_FILTER_NEAREST      = GL_NEAREST
    TEXTURE_FILTER_LINEAR       = GL_LINEAR

    TEXTURE_WRAP_CLAMP          = GL_CLAMP
    TEXTURE_WRAP_CLAMP_TO_EDGE  = GL_CLAMP_TO_EDGE
    TEXTURE_WRAP_REPEAT         = GL_REPEAT

    DEPTH_TEST_CURRENT          = "depthTestCurrent"
    DEPTH_TEST_ALWAYS           = GL_ALWAYS
    DEPTH_TEST_NEVER            = GL_NEVER
    DEPTH_TEST_EQUAL            = GL_EQUAL
    DEPTH_TEST_NOTEQUAL         = GL_NOTEQUAL
    DEPTH_TEST_LESSER           = GL_LESS
    DEPTH_TEST_TYPE_LEQUAL      = GL_LEQUAL
    DEPTH_TEST_TYPE_GREATER     = GL_GREATER
    DEPTH_TEST_TYPE_GEQUAL      = GL_GREATER

    def __init__(self):
        raise NotImplementedError("Konstans osztaly")




class GfxContext(object):
    """
    @raise SingletonClassError: Az osztály csak egyszer példányosítható
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(GfxContext, cls).__new__( cls, *args, **kwargs)
            return cls._instance
        else:
            raise SingletonClassError("Csak egyszer példányosítható!")

    def __init__(self):
        """
        GfxContext inicilializálása
        """
        pass

    @classmethod
    def getInstance(cls):
        """
        Az egyetlen GfxContext példány lekérése

        @return:    GfxContext példány
        @rtype:     C{GfxContext}
        """
        return cls._instance


    def drawPic2D(self, x, y, width, height, texture=None):
        """
        2D-s szabályos négyszögalakú poligon rajzolása textúrával

        @param  x:          A bal felső sarokpont x koordinátája
        @type   x:          C{float}
        @param  y:          A bal felső sarokpont y koordinátája
        @param  y:          C{float}
        @param  width:      A négyszög szélessége
        @type   width:      C{float}
        @param  height:     A négyszög magassága
        @type   height:     C{float}
        @param  texture:    A négyszögre húzott textúra C{default} None
                            None esetén nem hasnálja a textúrázást
        """
        self.color(1.0, 1.0, 1.0, 1.0)
        if texture != None:
            ActiveTextureUnit(Gfx.TEXTURE_UNIT_0)
            BindTexture(Gfx.TEXTURE_2D, texture)

        self.Begin(Gfx.TRISTRIP)
        self.TexCoord(0.0, 0.0)
        self.Vertex(x, y)
        self.TexCoord(0.0, 1.0)
        self.Vertex(x, y + height)
        self.TexCoord(1.0, 0.0)
        self.Vertex(x + width, y)
        self.TexCoord(1.0, 1.0)
        self.Vertex(x + width, y + height)
        self.End()

class GLContext(GfxContext):
    """
    Az OpenGL becsomagolása
    """

    def __init__(self, IOContext=None):
        GfxContext.__init__(self)

        self.__view = Viewport()
        self.__matrix = GLContext.GfxMatrix()
        self.__currTextureUnit = Gfx.TEXTURE_UNIT_0
        self.__curTextures = dict(zip(xrange(Gfx.TEXTURE_UNIT_0, Gfx.TEXTURE_UNIT_9), (None,)*Gfx.NUM_TEXTURE_UNITS))

        self.__fontList = None
        self.__fontTexture = None

        # set shader pointers to NULL
        self.normalmap_shader = None
        self.normalmap_vshader = None

        Text()

    @property
    def matrix(self):
        return self.__matrix

    @property
    def viewport(self):
        return self.__view

    def glInit(self):
        self.__checkEXT()
        self.__setupGL()

        print ("GfxDriverGL initialized")


    def __checkEXT(self):
        """
        A felhasznált OpenGL függvények elérhetőségének ellenőrzése
        """
        try:
            self.begin      = glBegin
            self.end        = glEnd
            self.clear      = glClear
            self.color      = glColor3f
            self.color4     = glColor4f
            self.vertex     = glVertex
            self.pointSize  = glPointSize
            self.lineWidth  = glLineWidth
        except Exception as e:
            raise IloExtensionError(e)


    def __setupGL(self):
        """
        OpenGL alapbeállítások elvégzése
        """
        try:
            glClearColor(0.0, 0.0, 0.0, 0.0)
            glClearDepth(1.0)
            glClearStencil(0)

            glShadeModel(GL_SMOOTH)

            glEnable(GL_CULL_FACE)
            glEnable(GL_NORMALIZE)
            glEnable(GL_COLOR_MATERIAL)
            glEnable(GL_TEXTURE_2D)
            glEnable(GL_DEPTH_TEST)
#            glEnable(GL_BLEND)
#            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            glDepthFunc(GL_LEQUAL) # so that multi-pass lightmapping works

            glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

            glCullFace(GL_BACK)
            glDisable(GL_CULL_FACE)
            glPolygonMode(GL_BACK, GL_FILL)
            glPolygonMode(GL_FRONT, GL_FILL)
            # set default projection matrix

            self.__buildFont()

            self.__view.setPerspectiveView()
            self.matrix.setMatrixMode(Gfx.MODELVIEW)
        except Exception as e:
            raise IloInitError(e)


    def beginRendering(self):
        """
        Leképezés előkészítése
        """
        self.matrix.setMatrixMode(Gfx.MODELVIEW)
        glClear(GL_COLOR_BUFFER_BIT |
                GL_DEPTH_BUFFER_BIT |
                GL_STENCIL_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)
        glClearStencil(0)
        glStencilMask(1)
        glClearDepth(1.0)
        glClearColor(0.0, 0.0, 0.0, 1.0)

        self.matrix.loadIdentity()

        #self.matrix.rotate(-90.0, 1.0, 0.0, 0.0)

    def endRendering(self):
        """
        Leképezés lezárása
        """
        glFlush()

    def beginMeshRenderPass(self):
        """
        Model leképezési fázis előkészítése
        """
        self.enableMaterials()
        glEnable(GL_VERTEX_ARRAY)

        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)

    def endMeshRenderPass(self):
        """
        Model leképezési fázis lezárása
        """
        glDisableClientState(GL_TEXTURE_COORD_ARRAY)
        glDisableClientState(GL_NORMAL_ARRAY)
        glDisableClientState(GL_VERTEX_ARRAY)

        glDisable(GL_VERTEX_ARRAY)
        self.disableMaterials()


    def enableMaterials(self):
        """
        Anyagminták használatának bekapcsolása
        """
        glEnable(GL_TEXTURE_2D)

    def disableMaterials(self):
        """
        Anyagminta használatának kikapcsolása
        """
        glDisable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, 0)
        glUseProgram(0)

    def __buildFont(self):
        """
        Font map betöltése és glList generálása a betűknek

        Felhasznált forrás:
            - U{Nehe: lesson 17 <http://nehe.gamedev.net/data/lessons/lesson.asp?lesson=17>}
        """
        glEnable(GL_TEXTURE_2D)
        if Config.hasValue("resource.fontmap"):
            self.__fontList = []
            self.__fontTexture = Texture(Config.getValue("resource.fontmap"))
            self.__fontTexture.bindTexture()
            self.__fontList = glGenLists(256)
            for i in xrange(256):
                cx = ( i % 16 ) / 16.0
                cy = ( i / 16 ) / 16.0
                glNewList(self.__fontList + i, GL_COMPILE)
                glBegin(GL_QUADS)
                glTexCoord2f(cx, 1-cy)
                glVertex2i(0, 0)
                glTexCoord2f(cx + 0.0625, 1-cy)
                glVertex2i(16, 0)
                glTexCoord2f(cx + 0.0625, 1-cy-0.0625)
                glVertex2i(16, 16)
                glTexCoord2f(cx, 1-cy-0.0625)
                glVertex2i(0, 16)
                glEnd()
                glTranslate(12,0,0)
                glEndList()
        glDisable(GL_TEXTURE_2D)


    def textRenderPass(self):
        """
        A beállított szövegobjektumok megjelenítése egymenetben
        a leképezés utólsó sakaszában (a takarás elkerüése érdekében)

        Felhasznált forrás:
            - U{Nehe: lesson 17 <http://nehe.gamedev.net/data/lessons/lesson.asp?lesson=17>}
        """
        if self.__fontTexture != None:
            self.enable2D(self.viewport.width, self.viewport.height)
            self.matrix.setMatrixMode(Gfx.MODELVIEW)
            glPushAttrib(GL_ALL_ATTRIB_BITS)
            glEnable(GL_TEXTURE_2D)
            glDisable(GL_LIGHTING)
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA,GL_ONE)
            self.__fontTexture.bindTexture()
            for item in Text.getInstance().textList:
                self.matrix.loadIdentity()
                glColor(*(item.color))
                #glScale(*(item.scale))
                glTranslate(item.x, item.y,0)
                glListBase(self.__fontList + (-32+(128*item.fontSet)))
                glCallLists(item.text)
            glPopAttrib()
            self.disable2D()

    def enable2D(self, width, height):
        """
        2D-s leképezés kezdete
        Ortgonális vetítés beállítása

        @param  width:  A 2D-s vetítési keret szélessége pixelben
        @type   width:  C{int}
        @param  height: A 2D-s vetítési keret magassága pixelben
        @type   width:  C{int}
        """
        self.matrix.setMatrixMode(Gfx.MODELVIEW)
        self.matrix.pushMatrix()
        self.matrix.loadIdentity()
        self.matrix.setMatrixMode(Gfx.PROJECTION)
        self.matrix.pushMatrix()
        self.matrix.loadIdentity()
        glOrtho(0, width, height, 0, 0, 1)
        glDisable(GL_DEPTH_TEST)
        #glDepthMask(GL_FALSE)

    def disable2D(self):
        """
        2D-s leképezés vége,
        Perspektívikus vetítés visszaállítása
        """
        self.matrix.setMatrixMode(Gfx.PROJECTION)
        self.matrix.popMatrix()
        self.matrix.setMatrixMode(Gfx.MODELVIEW)
        self.matrix.popMatrix()
        glEnable(GL_DEPTH_TEST)
        #glDepthMask(GL_FALSE)

    def activeTextureUnit(self, texture_unit):
        """
        Adott Textúra egység aktiválása, több szintű textúrázás esetén

        @param  texture_unit:   A beállítantandó textúrázási szint
        @type   texture_unit:   C{GLuint}
        """
        if self.__currTextureUnit == unit:
            return

        if (unit != GL_TEXTURE0 and not self.multitexture) or (unit >= NUM_TEXTURE_UNITS):
            return

        glActiveTextureARB(unit)
        glClientActiveTextureARB(unit)
        self.__currTextureUnit = unit


    class GfxMatrix(object):
        """
        OpenGL mátrixok kezelése

        Mátrixok beállítása, utoljára használt visszaállítása
        Mozgatás, forgatás, skálázás,
        """
        _instance = None

        __curMatrix = None
        __prevMatrix = None

        def __new__(cls, *args, **kwargs):
            if not cls._instance:
                cls._instance = super(GLContext.GfxMatrix, cls).__new__( cls, *args, **kwargs)
                return cls._instance
            else:
                raise SingletonClassError("Csak egyszer példányosítható!")

        def __init__(self):
            """
            GfxMatrix inicializálása
            """
            self.pushMatrix     = glPushMatrix
            self.popMatrix      = glPopMatrix
            self.setMatrixMode  = glMatrixMode
            self.translate      = glTranslate
            self.scale          = glTranslate
            self.rotate         = glRotate

        def __log(self, newType):
            """
            Utoljára használt mátrixtípus mentése

            @param  newType:  Az új használandó mátrix típus
            """
            GfxMatrix.__prevMatrix = GfxMatrix.__curMatrix
            GfxMatrix.__curMatrix = newType

        def prevMatrix(self):
            """
            Az utóljára használt mátrixtípus visszaállítása
            """
            glMatrixMode( GfxMatrix.___prevMatrix )
            GfxMatrix.__log(GfxMatrix.___prevMatrix)

        def getMatrix(self, type):
            """
            Megadott típusú mátrix lekérdezése

            @param type:    A kért mátrix típusa
            """
            if type == GL_PROJECTION:
                return Matrix4x4(glGetDoublev(GL_PROJECTION_MATRIX))
            if type == GL_MODELVIEW:
                return Matrix4x4(glGetDoublev(GL_MODELVIEW_MATRIX))
            if type == GL_TEXTURE:
                return Matrix4x4(glGetDoublev(GL_TEXTURE_MATRIX))

        def setMatrix(self, matrix, type = None ):
            """
            Adott típusú mátrix beállítása

            @param  matrix:  A beállítandó mátrix
            @param  type:    A beállítandó mátrix típusa
            """
            if type :
                glMatrixMode( type )
            if isinstance(matrix, Matrix4x4):
                glLoadMatrixd( matrix.T )
            else:
                glLoadMatrixd( matrix )

        def multiplyMatrix(self, matrix, type = None):
            """
            A megadott típusú openGL mátrixra jobbról rászorzunk az adott
            mátrixxal

            @param  matrix:  A szorzó mátrix
            @param  type:    A szorzandó openGL mátrix típusa
            """
            if type :
                glMatrixMode( type )
            glMultMatrixd( matrix )

        def loadIdentity(self, type = None):
            """
            Egységmátrix beállítása a megadott típusú openGL mátrixra

            @param  type:   OpenGL mátrix típus
            """
            if type :
                glMatrixMode( type )
            glLoadIdentity()

#-----------------------------------------GETTER/SETTER-------------------------
        @property
        def currentMatrix(self):
            return GfxMatrix.__curMatrix

        @property
        def previewMatrix(self):
            GfxMatrix.__prevMatrix



class Viewport(object):
    """
    Az OpenGL nézőpontot kezelő Singleton osztály
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Viewport, cls).__new__( cls, *args, **kwargs)
            return cls._instance
        else:
            raise SingletonClassError("Csak egyszer példányosítható!")

    def __init__(self):
        """
        Viewport inicializálása
        """
        self.__fov       = Config.getValue("projection.fov")
        self.__ration    = 1.0
        self.__nearPlane = 0.05
        self.__farPlane  = 2000.0
        self.__x = 0
        self.__y = 0
        self.__width = 1
        self.__height = 1

    def setViewport(self, x, y, width, height, infFrustun=False):
        """
        Nézet beállítása

        @param  x:          Az openGL nézet x koordinátája a főablakban ablakban
        @param  y:          Az openGL nézet y koordinátája a főablakban ablakban
        @param  width:      Az openGL nézet szélessége
        @param  height:     Az openGL néze magasság
        @param  infFrustun: Végtelen nézőpont beállítása
        """
        height = max(height, 1)
        self.__x, self.__y, self.__width, self.__height = x, y, width, height;
        self.__ration = width/height

        glViewport(x, y, width, height)
        self.setPerspectiveView()
        if infFrustun :
            self.__setInfiniteFrustum()

    def setPerspectiveView(self):
        """
        Perspektív vetítés beállítása
        """
        GLContext.getInstance().matrix.loadIdentity(Gfx.PROJECTION)
        gluPerspective(self.__fov, self.__ration, self.__nearPlane, self.__farPlane)

    def getNear(self):
        """
        Közeli sík visszaadása

        @return near sík koordinátái
        """
        y = self.__nearPlane * math.tan(self.__fov / 2)
        x = y * self.__width / self.__height
        z = self.__nearPlane

        return x, y, z

    def getInfiniteFrustumMatrix(self):
        """
        Végtelen vetítési mátrix számítása

        @return vetítési mátrix (4x4)
        """
        x, y, z = self.getNear()

        left    = -x
        right   =  x
        top     =  y
        bottom  = -y
        nearval =  z

        x = (2.0 * nearval)  / (right - left)
        y = (2.0 * nearval)  / (top   - bottom)
        a = (right + left)   / (right - left)
        b = (top   + bottom) / (top   - bottom)
        c = -2.0 * nearval

        return [[x,   0.0,    a, 0.0],
                [0.0,   y,    b, 0.0],
                [0.0, 0.0, -1.0,   c],
                [0.0, 0.0, -1.0, 0.0]]

    def __setInfiniteFrustum(self):
        """
        Végtelen vetítési nézet beállítása
        """
        GLContext.getInstance().matrix.setMatrix(self.getInfiniteFrustumMatrix(),Gfx.PROJECTION)

#-----------------------------------------GETTER/SETTER-------------------------

    @property
    def size(self):
        return (self.__x, self.__y, self.__width, self.__height)

    @property
    def fov(self):
        return self.__fov

    @fov.setter
    def fov(self, value):
        self.__fov = value
        self.resetViewport()

    @property
    def nearPlane(self):
        return self.__nearPlane

    @nearPlane.setter
    def nearPlane(self, value):
        self.__nearPlane = value
        self.resetViewport()

    @property
    def x (self):
        return self.__x

    @property
    def y (self):
        return self.__y

    @property
    def width (self):
        return self.__width

    @property
    def height (self):
        return self.__height

