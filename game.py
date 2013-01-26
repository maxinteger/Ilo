# -*- coding: utf -*-

__author__="Vadasz Laszlo"
__date__ = "2009.07.20. 22:06:39"

from ilo.render.particle import *
from PyQt4.QtCore import Qt
from ilo.engine import IloEngine
from ilo.messages.events import *
from ilo.system.text import Text
from ilo.system.lights import LightLibraly

class Game (IloEngine):
    """Teszt játék"""
    def __init__(self):
        self.fok = 0
        IloEngine.__init__(self)
        
    def preLoad(self):
        self.cam = self.glContext.camera
        self.cam.moveTo(0.0,-40.0,20.0)
        self.cam.rotateX = 20
        self.addEventListener(KeyboardEvent.PRESS, self.keyEvent)
        self.addEventListener(Event.ENTER_FRAME, self.enterframe)
        self.addEventListener(MouseEvent.MOVE, self.mouseEvent)

        self.t = Text.getInstance().addText(10, 10, "hello\n world")
        self.rot = Text.getInstance().addText(10, 25, "R")
        self.coo = Text.getInstance().addText(10, 40, "C")
        self.level = self.libraly.loadSceneXML('data/mapdata.xml')

        self.addElement(self.level, "level")

        self.light = LightLibraly.getInstance()
         #self.light.globalAmbient([0.5,0.5,0.5,1.0])

        self.light.turnOnLights()

        self.l1 = self.light.addLight()

        self.l1.diffuse = [1.0,1.0,1.0,1.0]
        self.l1.lightIntesity = 100
        self.l1.coord.z = 40
        self.l1.setSpot((0.0,0.0,-10.0), 10.0)
        self.addElement(self.l1, "light_1")

        self.particle1 = BaseParticleSystem("first", 10, "data/texture/fust.bmp")
        self.addElement(self.particle1, 'p1')
        self.particle2 = BaseParticleSystem("first", 10, "data/texture/fust.bmp")
        self.addElement(self.particle2, 'p2')

        self.particle1.coord = (-2.0, 2.25, 10.0)
        self.particle2.coord = (2.0, 2.25, 10.0)
        self.particle1.scale = (0.2, 0.2, 0.2)
        self.particle2.scale = (0.2, 0.2, 0.2)
        self.particle1.angle.z = 45
        self.particle2.angle.z = -45


    def enterframe(self, event):
        self.fok += 1
        #self.level.angle.z = self.fok
        self.t.text = "fps: " + str(self.getCurFPS())

    def keyEvent(self, event):
        if Qt.Key_Escape == event.key :
            self.window.close()

        if Qt.Key_A == event.key:
            self.cam.moveTo(-2.0,0.0,0.0)
        if Qt.Key_D == event.key:
            self.cam.moveTo(2.0,0.0,0.0)

        if Qt.Key_W  == event.key:
            self.cam.moveTo(0.0,2.0,0.0)
        if Qt.Key_S  == event.key:
            self.cam.moveTo(0.0,-2.0,0.0)

        if Qt.Key_Left == event.key:
            self.l1.coord.x -=2
        if Qt.Key_Right == event.key:
            self.l1.coord.x += 2
        if Qt.Key_Up  == event.key:
            self.l1.coord.z += 2
        if Qt.Key_Down  == event.key:
            self.l1.coord.z -= 2

        if Qt.Key_Q == event.key:
            self.cam.rotateY = 5
        if Qt.Key_E == event.key:
            self.cam.rotateY = -5

        if Qt.Key_L == event.key:
            self.light.switchLight()

        if Qt.Key_T == event.key:
            self.cam.flyTo(1.0)
        if Qt.Key_G == event.key:
            self.cam.flyTo(-1.0)

        self.rot.text = "R x: %d; y:%d; z:%d" % (
            self.cam.rotateX,
            self.cam.rotateY,
            self.cam.rotateZ
        )

        self.coo.text = "C x: %d; y:%d; z: %d" % tuple(self.cam.position)

        if event.key == 16777219:
            self.t.text = self.t.text[:-1]
        elif event.key < 256 and (event.key not in [ord(x)  for x in "AWDSQE"]):
            self.t.text += chr(event.key)

            
    def mouseEvent(self, event):
        self.cam.rotateX =  event.delta[1]
        self.cam.rotateZ = -event.delta[0]

        self.rot.text = "R x: %d; y:%d; z:%d" % (
        self.cam.rotateX,
        self.cam.rotateY,
        self.cam.rotateZ)



if __name__ == '__main__':
    if True:
        Game()
    else:
        import hotshot, hotshot.stats, test.pystone
        prof = hotshot.Profile("stones.prof")
        prof.runcall(main)
        prof.close()

        stats = hotshot.stats.load("stones.prof")
        stats.strip_dirs()
        stats.sort_stats('time', 'calls')
        stats.print_stats(20)


