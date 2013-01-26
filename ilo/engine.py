# -*- coding: utf -*-

__author__="Vadasz Laszlo"
__date__ ="2009.08.19. 11:12:03"

from PyQt4 import QtGui, QtCore, QtOpenGL

from ilo.config import Config
from ilo.structs.libraly import *
from ilo.render.glwidget import *
from ilo.gui.windows import MainWindow
from ilo.messages.events import Event
from ilo.render.display import RenderScene


class IloEngine(RenderScene):
    """
    Az Ilo API főosztálya

    Ebból az osztályból kell származtatni a játék fő osztályát!
    Az osztály összfogja a főbb komponenseket
        - grafikus ablak
        - OpenGL környezet
        - időzítés
        - scene
    melyekhez egyszerű és a lehető legközvetlenebb felületet biztosítja
    """

    __slots__ = ('__application', '__window', '__context', '__timer', '__libraly',
                 '__fps', '__curFPS', '__countFPS', '__HiddenMouse')

    def __init__(self):
        """
        Ilo API inicilaizálása

         1. az ősosztály inicilaizálása
         2. az alkalmazás és az ablak létrezozása
         3. OpneGL környezet létrehozása
         4. az alkalmazás indítása
        """

        RenderScene.__init__(self)

        Config.loadConfigXML("data/config.xml", True)
        
        self.__initEngine()
        self.__initWindows()
        self.__initGLContext()

        self.__application.exec_()


    def preLoad(self):
        """
        Adatok előtöltése szolgátó metódus melynek felülírásával betölthetjük
        az program indításakor szükséges adatokat
        """
        assert True ("Az adatok előtöltéséhez felül kell írni ezt a függvényt!")


    def __initEngine(self):
        """
        A motor alap beállításainak elvégzése
        """
        self.__fps          = Config.getValue("engine.fps")                     #:@ivar: Maximális FPS szám
        self.__curFPS       = -1                                                #:@ivar: Aktuális FPS szám
        self.__countFPS     = 0                                                 #:@ivar: FPS számláló
        self.__HiddenMouse  = False                                             #:@ivar: Az egér mutató láthatóságának állapota


    def __initWindows(self):
        """
        Az alkalmazás, a főablak és a főidőzítő inicilaizálása
        """

        self.__application = QtGui.QApplication(['Ilo engine'])                 #:@ivar: Az alkalmazás
        self.__window      = MainWindow()                                       #:@ivar: A főablak
        self.__window.resize(Config.getValue("window.width"),
                             Config.getValue("window.height"))
        self.__window.show()

        self.__timer = QtCore.QTimer(self.__window)                             #:@ivar: A fő időzítő


    def __initGLContext(self):
        """
        Az OpenGL környezeti paraméterek beállítása
        Az OpenGL környezet létrehozása
        A visszahívó függvény beállítása
        """

        glFormat = QtOpenGL.QGLFormat()
        glFormat.setDirectRendering(True)
        glFormat.setDoubleBuffer(True)
        glFormat.setDepth(True)
        glFormat.setStencil(True)
        glFormat.setStencilBufferSize(Config.getValue("system.stencil_bits"))
        glFormat.setSampleBuffers(True)
        glFormat.setSamples(0)
        glFormat.setSwapInterval(0)
        QtOpenGL.QGLFormat.setDefaultFormat(glFormat)

        self.__context = GLWidget(self.__window, self)                          #:@ivar: Grafikus környezet
        self.__window.setGLContext(self.__context)
        
        self.__context.disp.addEventListener(Event.GL_INIT,      self.__onGLinited)
        self.__context.disp.addEventListener(MouseEvent.CLICK,   self.__eventReflection)
        self.__context.disp.addEventListener(MouseEvent.RELEASE, self.__eventReflection)
        self.__context.disp.addEventListener(MouseEvent.MOVE,    self.__mouseMove)
        self.__context.disp.addEventListener(MouseEvent.WHEEL,   self.__eventReflection)
        self.__window.disp.addEventListener(KeyboardEvent.PRESS, self.__eventReflection)


    def __onGLinited(self, event):
        """
        Eseménykezelő metódus
        Akkor hajtódik végre amikor az openGL környezet sikeresen
        inicializálódott és kész a parancsok értelmezésére
        
        @param  event:  esemény objektum
        @type   event:  C{Event}
        """
        self.__context.disp.removeEventListener(Event.GL_INIT, self.__onGLinited)

        self.__libraly = Libraly()                                              #:@ivar: Adattár

        self.__window.connect(self.__timer, QtCore.SIGNAL('timeout()'), self.__context.updateGL)
        self.__window.connect(self.__timer, QtCore.SIGNAL('timeout()'), self.__enterFrame)
        self.__window.connect(self.__timer, QtCore.SIGNAL('timeout()'), self.__countFrame)
        self.__timer.start(1000 / self.__fps)

        self.preLoad()


    def __enterFrame(self):
        """
        Ütemező
        """
        self.dispatchEvent(Event(Event.ENTER_FRAME))


    def __mouseMove(self, event):
        """
        Az egérmozgást követő eseményvezérlő bővítése, az egér mozgásterének
        korlátozására

        @param  event:  esemény objektum
        @type   event:  C{MouseEvent}
        """
        _mx = QtGui.QCursor.pos().x()
        _my = QtGui.QCursor.pos().y()
        _wx = self.__window.x() + 5
        _wy = self.__window.y() + 25
        _ww = _wx + self.__window.width() -10
        _wh = _wy + self.__window.height()-30
        
        #X
        if _mx < _wx:
            QtGui.QCursor.setPos(_ww, _my)
            event.pos.x = -1
        elif _mx > _ww:
            QtGui.QCursor.setPos(_wx, _my)
            event.pos.x = 1
        #Y
        if _my < _wy:
            QtGui.QCursor.setPos(_mx, _wh)
            event.pos.y = -1
        elif _my > _wh:
            QtGui.QCursor.setPos(_mx, _wy )
            event.pos.y = 1

        self.dispatchEvent(event)


    def __eventReflection(self, event):
        """
        Esemény közvetítő

        @param  event:  esemény objektum
        @type   event:  C{Event}
        """
        if self.hasEventListener(event.type):
            self.dispatchEvent(event)

    def __countFrame(self):
        """
        FPS szám léptető
        """
        self.__countFPS += 1

    def __calcFPS(self):
        """
        FPS kiszámítása
        """
        self.__curFPS = self.__countFPS
        self.__countFPS = 0

    def getCurFPS(self):
        """
        Legutóbbi FPS szám lekérdezése
        Ha az FPS számláló nem volt inciaéizálva akkor az is itt történik
        """
        if self.__curFPS == -1:
            self.__fps_timer = QtCore.QTimer(self.__window)
            self.__fps_timer.start(1000)
            self.__window.connect(self.__fps_timer, QtCore.SIGNAL('timeout()'),\
                                  self.__calcFPS)
            self.__curFPS = 0
        return self.__curFPS

    @property
    def application(self):
        """
        A futási környzet
        """
        return self.__application

    @property
    def window(self):
        """
        A programablak
        """
        return self.__window

    @property
    def glContext(self):
        """
        A leképező környezet
        """
        return self.__context

    @property
    def libraly(self):
        return self.__libraly

    @property
    def vertSync(self):
        """
        Várakozás a képrenyő vízszintes sor frissítésére
        """
        return QtOpenGL.QGLFormat.defaultFormat().swapInterval() != 0

    @vertSync.setter
    def vertSync(self, value):
        glFormat = QtOpenGL.QGLFormat.defaultFormat()
        if value:
            glFormat.setSwapInterval(1)
        else:
            glFormat.setSwapInterval(0)
        QtOpenGL.QGLFormat.setDefaultFormat(glFormat)

    @property
    def fps(self):
        """
        Maximális FPS szám lekérdezése éb beállítása
        """
        return self.__fps

    @fps.setter
    def fps(self, value):
        if value > 0 :
            self.__fps = value
            self.__timer.stop()
            self.__timer.start(1000 / value)
        else:
            raise IloNumberError("Az FPS szám csak nullánal nagyobb lehet!")
            

    @property
    def hideMouse(self):
        """
        Az egér mutató láthatóságának állapota C{True} ha látható különben C{False}
        """
        return self.__HiddenMouse

    @hideMouse.setter
    def hideMouse(self, value):
        if value :
            self.__HiddenMouse = True
            self.__application.setOverrideCursor( QtGui.QCursor( QtCore.Qt.BlankCursor ) )
        else:
            self.__application.restoreOverrideCursor()
            self.__HiddenMouse = False

