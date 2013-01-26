# -*- coding: utf -*-

__author__="Vadasz Laszlo"
__date__ ="2010.04.08. 17:34:03"


from random import *

from OpenGL.raw.GL.constants import *
from OpenGL.raw.GL import *
from OpenGL.GL import *

from ilo.render.display import *
from ilo.structs.vector import *
from ilo.structs.color import Color

"""
Részecskerendszer modul, mely tartalmazza az részecske osztályt és az alap
részecskegeneráló osztályt
"""

class BaseParticleSystem(RenderObject):

    """
    Alap részecske leképező osztály, mely a C{RenderObject}-ből származik
    és képes a részekék paraméterezett előállítására, a részecskék kezelésére és
    azok leképzésére.
    """

    __slots__ = RenderObject.__slots__ +\
                ('numOfParticle', 'life', 'size', 'cSpeed', 'sSpeed', 'aSpeed',
                 'particleItem', 'particleTex', 'particles', 'tick')

    def __init__(self, name, numOfParticle, texture):
        """
        BaseParticleSystem inicializálása

        @param  name:           A részecskerendszer neve
        @type   name:           C{string}
        @param  numOfParticle:  A részecskék száma
        @type   numOfParticle:  C{int}
        @param  texture:        A részecskékhez rendelt textúra elérési útvonala
        @type   texture:        C{String}
        """
        RenderObject.__init__(self, name, None, None)

        self.numOfParticle  = numOfParticle                                     #:@ivar: A részecskék száma
        self.tick           = 0                                                 #:@ivar: Leképezések száma
        self.life           = (100, 500, 1)                                     #:@ivar: A részecskék élete (min, max, lépték)
        self.size           = (50,  150)                                        #:@ivar: A részecskék mérete (min, max)
        self.cSpeed         = (0.1,  1.0)                                       #:@ivar: A részecskék mozgási sebessége (min, max)
        self.sSpeed         = (0.01, 0.1)                                       #:@ivar: A részecskék növekedési sebessége (min max)
        self.aSpeed         = (0.5,  5.0)                                       #:@ivar: A részecskék forgási sebessége (min, max)
        self.particleItem   = 0                                                 #:@ivar: Részecske displayList
        self.particleTex    = Texture(texture)                                  #:@ivar: Részecske anyagjellemző
        self.particles      = []                                                #:@ivar: Részecskék listája
        
        for i in xrange(self.numOfParticle):
            self.particles.append(self.__setParticle(Particle(), i))

        self.__makeParticleItem()


    def render__(self):
        """
        Részecskák leképzése
        """
        self.tick += 1
        # @type i Particle
        glPushMatrix()
        glPushAttrib(GL_ALL_ATTRIB_BITS)

        glEnable(GL_TEXTURE_2D)
        #glDisable(GL_LIGHTING)
        glEnable(GL_BLEND)
        glEnable( GL_POLYGON_OFFSET_FILL )
        glBlendFunc(GL_SRC_ALPHA, GL_ONE)

        glTranslate(*self._coord)
        glRotate(self._angle[0],1.0, 0.0, 0.0)
        glRotate(self._angle[1],0.0, 1.0, 0.0)
        glRotate(self._angle[2],0.0, 0.0, 1.0)
        glScale(*self._scale)
        
        self.particleTex.bindTexture()

        for i in self.particles:
            if i.active :
                if i.life > 0.0:
                    i.step()
                    
                    glPushMatrix()

                    glTranslate(*i.coord)
                    glRotate(i.angle.x,1.0, 0.0, 0.0)
                    glRotate(i.angle.y,0.0, 1.0, 0.0)
                    glRotate(i.angle.z,0.0, 0.0, 1.0)
                    glScale(*i.scale)
                    glColor(*i.color.list)
                    glPolygonOffset( -i.id, -i.id )

                    glCallList(self.particleItem)

                    glPopMatrix()
                else:
                    self.__setParticle(i)

        glPopAttrib()
        glPopMatrix()


    def __setParticle(self, item, id=None):
        """
        Új részecskék inicializálása

        @param  item:   A beállítandó részecske
        @type   item:   C{Particle}
        @param  id:     A részeke sorszáma
        @type   id:     C{int}
        """
        # @type item Particle
        if id != None: item.id = id
        item.color      = Color([1.0, 1.0, 1.0, 1.0])
        item.life       = 1.0
        item.fade       = randrange(10, 100)/5000.0
        item.active     = True
        item.coord      = Vector3.zeros()
        item.cSpeed     = Vector3([0.0,0.0,.1])
        item.scale      = Vector3([0.1,0.1,0.1])
        item.sSpeed     = Vector3([randrange(*self.size)/100.0 * item.fade ]*3)
        item.angle      = Vector3([0.0,random()*180, 0.0])
        item.aSpeed     = Vector3([0.0, randrange(-10, 10)/50.0, 0.0])
        #item.angle.z    = random()*180

        return item


    def __makeParticleItem(self):
        """
        Részecske displayList létrehozása
        """
        glPushAttrib(GL_ALL_ATTRIB_BITS)
        glEnable(GL_TEXTURE_2D)
        self.particleTex.bindTexture()
        self.particleItem = glGenLists(1)
        glNewList(self.particleItem, GL_COMPILE)
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex3f  (-5.0, 0.0, -5.0)

        glTexCoord2f(1.0,0.0)
        glVertex3f  (5.0, 0.0, -5.0)

        glTexCoord2f(1.0,1.0)
        glVertex3f  (5.0, 0.0, 5.0)

        glTexCoord2f(0.0,1.0)
        glVertex3f  (-5.0, 0.0, 5.0)
        glEnd()
        glEndList()
        glDisable(GL_TEXTURE_2D)
        glPopAttrib()




class Particle(object):
    """
    Részecske osztály
    """

    __slots__ = ('id', 'active', 'life', 'fade', 'color',
                 'coord', 'cSpeed',
                 'scale', 'sSpeed',
                 'angle', 'aSpeed')

    def __init__(self):
        """
        Particles inicilaizálása
        """
        self.id         = 0                                                     #:@ivar: A részecske egyedi azonosítója a rendszeren belül
        self.active     = True                                                  #:@ivar: A részecske aktív C{True} külöben C{False}
        self.life       = 0                                                     #:@ivar: A részecske aktuális élettartama, mely egy 0 és 1 közti szám ahol az 1 az új a 0 a halott elem
        self.fade       = 0                                                     #:@ivar: Az részecske életének csökkenésének a léptéke
        self.color      = Color([1.0,1.0,1.0,1.0])                              #:@ivar: A részecske színe (RGBa)

        self.coord      = Vector3([0.0,0.0,0.0])                                #:@ivar: A részecske aktuális koordinátái
        self.cSpeed     = Vector3([0.0,0.0,0.0])                                #:@ivar: A részecske mozgási sebessége
        self.scale      = Vector3([0.0,0.0,0.0])                                #:@ivar: A részecske aktuális mérete
        self.sSpeed     = Vector3([0.0,0.0,0.0])                                #:@ivar: A részecske átméreteződésének a sebessége
        self.angle      = Vector3([0.0,0.0,0.0])                                #:@ivar: A részecske aktuális elfordulása
        self.aSpeed     = Vector3([0.0,0.0,0.0])                                #:@ivar: A részecske elfordulásának a sebessége

    def step(self):
        """
        A részecske következő életciklsának számítása
        """
        self.life       -= self.fade
        self.coord      += self.cSpeed
        self.scale      += (self.sSpeed*1.01)
        self.angle      += self.aSpeed
        self.color.a    = self.life
#        self.color.r    = self.life
#        self.color.g    = self.life
        
        return self.life