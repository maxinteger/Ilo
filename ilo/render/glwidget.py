# -*- coding: utf -*-

__author__="Vadasz Laszlo"
__date__ = "2009.07.20. 22:42:06"

from PyQt4.QtOpenGL import *
from OpenGL.GL import *
from OpenGL.GLU import *
from ilo.messages.events import *
from ilo.system.gfx import *
from ilo.system.camera import Camera
from ilo.system.lights import LightLibraly
from ilo.structs.vector import Vector2

class GLWidget(QGLWidget):
    """
    OpenGL megjelenítő

    A QGLWidget-ből származtatott OpenGL megjelenítő.
    Inicializálja az OpenGL alrendszert, és itt kezdődik meg a grafikus elemek
    leképezése, többmenetben.
    A grafikus területen bekövetkezett egéreseményeket is itt kezeli a rendszer.
    """

    __slots__ = ('gfx', 'camera', 'disp', '_scene',
                 '__mb1_pressed', '__mb2_pressed', '__mb4_pressed'
                 '__mouse_prev_pos')

    def __init__(self, parent, scene):
        """
        OpenGL megjelenítő inicilaizálása

        @param  parent: Qt szülő elem
        @type   parant: C{QWidget}
        @param  scene:  A gyökér scene objektum
        @param  scene:  C{IloEngine}
        """
        QGLWidget.__init__(self, parent)

        self.disp = EventDispatcher()                                           #:@ivar: Eseménydobó objektum

        self.gfx = GLContext()                                                  #:@ivar: Grafikus mag elérése
        self.camera = Camera()                                                  #:@ivar: Kamera elérése
        self.__scene = scene                                                    #:@ivar: Fő szín elérése

        self.__mb1_pressed = False                                              #:@ivar: A balegérgom le van nyomva
        self.__mb2_pressed = False                                              #:@ivar: A jobbegérgomb le van nyomva
        self.__mb4_pressed = False                                              #:@ivar: A középsőegérgomb le van nyomva
        self.__mouse_prev_pos = Vector2((0,0))                                  #:@ivar: Az egér előző pozííciója

        self.setAutoBufferSwap(True)
        self.setMouseTracking(True)


    def initializeGL(self):
        """
        Az OpenGL környezet inicializálása
        """
        self.gfx.glInit()
        self.lights = LightLibraly(self.__scene)
        
        self.disp.dispatchEvent(Event(Event.GL_INIT))


    def paintGL(self):
        """
        Aktuális képkocka leképezése
        """
        self.gfx.beginRendering()

        #self.camera.updateFrustum()
        self.camera.update()
        self.gfx.matrix.multiplyMatrix(self.camera.matrix.T)

        self.gfx.beginMeshRenderPass()
        self.__scene.render__()
        self.gfx.endMeshRenderPass()

        self.gfx.textRenderPass()

        self.gfx.endRendering()


    def resizeGL(self, width, height):
        """
        Ablakátméretezés

        Eseménykezelő mely az openGL környezet átméretezésekor hívódik meg

        @param  width:  Az ablak új szélességa
        @type   width:  C{int}
        @param  height: Az ablak új magassága
        @type   height: C{int}
        """
        self.gfx.viewport.setViewport(0, 0, width, height)
        self.gfx.matrix.setMatrixMode(Gfx.MODELVIEW)

        self.disp.dispatchEvent(WindowEvent(WindowEvent.RESIZE, 0, 0, width, height))




    def mousePressEvent(self, event):
        """
        QOpenGL egér gomb lenyomás eseménykezelő

        A kapott eseményt tovább dobja, a beépített eseménykezelőn keresztül egy
        C{MoseEvent} formájában.

        @param  event:  Egéresemény
        @type   event:  C{QMouseEvent}
        """
        pos = Vector2((event.pos().x(),event.pos().y()))
        self.disp.dispatchEvent(MouseEvent(MouseEvent.CLICK,
                                           event.button(),
                                           pos,
                                           pos - self.__mouse_prev_pos,
                                           0,
                                           False,
                                           False,
                                           False))

        self.__m_pos = [pos.x, pos.y]
        if event.button() == 1:
            self.__pause = True
            self.doPicking(pos.x, pos.y)
            self.__pause = False
        if event.button() == 2:
            self.__mb2_pressed = True
        elif event.button() == 4:
            self.__mb4_pressed = True



    def mouseReleaseEvent(self, event):
        """
        QOpenGL egér gomb felengedés eseménykezelő

        A kapott eseményt tovább dobja, a beépített eseménykezelőn keresztül egy
        C{MoseEvent} formájában.

        @param  event:  Egéresemény
        @type   event:  C{QMouseEvent}
        """
        pos = Vector2((event.pos().x(),event.pos().y()))
        self.disp.dispatchEvent(MouseEvent(MouseEvent.RELEASE,
                                           event.button(),
                                           pos,
                                           pos - self.__mouse_prev_pos,
                                           0,
                                           False,
                                           False,
                                           False))
        if event.button() == 1:
            pass
            #self.__pause = False
        if event.button() == 2:
            self.__mb2_pressed = False
        elif event.button() == 4:
            self.__mb4_pressed = False

    def mouseMoveEvent(self, event):
        """
        QOpenGL egér mozgás eseménykezelő

        A kapott eseményt tovább dobja, a beépített eseménykezelőn keresztül egy
        C{MoseEvent} formájában.

        @param  event:  Egéresemény
        @type   event:  C{QMouseEvent}
        """
        pos = Vector2((event.pos().x(),event.pos().y()))
        self.disp.dispatchEvent(MouseEvent(MouseEvent.MOVE,
                                           event.button(),
                                           pos,
                                           pos - self.__mouse_prev_pos,
                                           0,
                                           False,
                                           False,
                                           False))

        self.__mouse_prev_pos = pos

        posx, posy = event.pos().x(), event.pos().y()
        
        if self.__mb2_pressed:
            pass
        elif self.__mb4_pressed:
            pass
        self.__m_pos = [posx, posy]


    def wheelEvent(self, event):
        """
        QOpenGL egér gomb körgő eseménykezelő

        A kapott eseményt tovább dobja, a beépített eseménykezelőn keresztül egy
        C{MoseEvent} formájában.

        @param  event:  Egéresemény
        @type   event:  C{QMouseEvent}
        """
        pos = Vector2((event.pos().x(),event.pos().y()))
        self.disp.dispatchEvent(MouseEvent(MouseEvent.WHEEL,
                                           -1,
                                           pos,
                                           pos - self.__mouse_prev_pos,
                                           event.delta(),
                                           False,
                                           False,
                                           False))
        self.__mouse_prev_pos = pos


    def doPicking(self, posx, posy, size = 100):

        x,y, width, height = self.gfx.viewport.size
        hits = [0] * 4
        view = [0] * 4

        selBuff = glSelectBuffer(128)
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()

        glRenderMode(GL_SELECT)

        glInitNames()
        glPushName(0)

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()

        glLoadIdentity()


        gluPickMatrix(posx, height - posy + x, 2,2, self.gfx.viewport.size)
        gluPerspective(45.0, width / height, 1.0, 425.0)

        self.paintGL()

        hits = glRenderMode(GL_RENDER)


        glMatrixMode(GL_PROJECTION)
        glPopMatrix()

        glMatrixMode(GL_MODELVIEW)

        glFlush()
