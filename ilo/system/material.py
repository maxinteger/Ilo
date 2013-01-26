# -*- coding: utf -*-

__author__="Vadasz Laszlo"
__date__ ="2010.02.24. 5:50:48"

import os.path
from xml.dom.minidom import *

from OpenGL.GL import *
from Image import open as imgOpen
from ilo.messages.exceptios import *
from ilo.config import Config

"""
Anyagjellemzők kezelésével foglalkozó modul
"""


class Material():
    """
    Anyagminta osztály

    A következő elemekből épül fel:
     - Anyagjellemzők:
        - ambient,
        - diffuse,
        - specular,
        - emission,
        - shininess
     - Bitmap textúra
     - Shader textúra
        - vertex shader
        - fragment shader
    """

    __slots__ = ('ambient', 'diffuse', 'specular', 'emission', 'shininess',
                 '__texture', '__shader')

    def __init__(self, ambient, diffuse, specular, emission, shininess):
        """
        Anyagminta iniciaéizálása
        Szín adatok beállítása

        @param  ambient:    Ambiens szín adatok
        @type   ambient:    C{List}
        @param  diffuse:    Diffuse szín adatok
        @type   diffuse:    C{List}
        @param  specular:   Specular szín adatok
        @type   specular:   C{List}
        @param  emission:   Emission azaz kibocsájtott fény szín adatai
        @type   emission:   C{List}
        @param  shininess:  Shininess azaz csillogási érték
        @type   shininess:  C{Float}
        """
        self.ambient   = ambient                                                #:@ivar: Ambiens szín adatok
        self.diffuse   = diffuse                                                #:@ivar: Diffuse szín adatok
        self.specular  = specular                                               #:@ivar: Specular szín adatok
        self.emission  = emission                                               #:@ivar: Emission azaz kibocsájtott fény szín adatai
        self.shininess = shininess                                              #:@ivar: Shininess azaz csillogási érték

        self.__texture   = None                                                 #:@ivar: Bitmap textúra tároló
        self.__shader    = None                                                 #:@ivar: Shader tároló

        
    def setTexture(self, texture):
        """
        Textúra hozzáadása az anyagmintához, ha engedélyezve vannak a
        C{bitmaptexture} a konfigurációban

        @param  texture:    Az anyagmintához kapcsolandó  textúra objektum
        @type   texture:    C{Texture}
        """
        if Config.getValue("render.bitmaptexture") and isinstance(texture, Texture):
            self.__texture = texture

    def setShader(self, shader ):
        """
        Shader hozzáadása az anyagmintához, ha engedélyezve vannak a C{shader}
        a konfigurációban

        @param  shader:  Az anyagmintához kapcsolandó shader objektum
        @type   shader: C{Shader}
        """
        if Config.getValue("render.shader") and isinstance(shader, Shader):
            self.__shader = shader


    def bindMaterial(self):
        """
        Anyagjellemzők használata
        Textúrák és shaderek bekapcsolása (C{bind})
        """
        glMaterialfv(GL_FRONT, GL_AMBIENT,   self.ambient)
        glMaterialfv(GL_FRONT, GL_DIFFUSE,   self.diffuse)
        glMaterialfv(GL_FRONT, GL_SPECULAR,  self.specular)
        glMaterialfv(GL_FRONT, GL_EMISSION,  self.emission)
        glMaterialf (GL_FRONT, GL_SHININESS, self.shininess)

        if self.__texture:
            self.__texture.bindTexture()
        else:
            Texture.unbindTexture()
            
        if self.__shader:
            self.__shader.bindShader()
        else:
            Shader.unbindShader()


    def remove(self):
        """
        Törli az anyagmintát a memóriából
        """
        if self.__texture:
            self.__texture.remove()
        if self.__shader:
            self.__shader.remove()




class Texture(object):
    """
    Bitmap textúra osztály

    Feladatai:
     - Bipmap adatok betöltése
     - openGL filterek alkalmazása
     - Textúra 'kötése' (C{bind}) és a kötés feloldása (C{unbind})
     - Textúra törlése, memória felszabadítás
    """

    __slots__ = ('imageFile', 'type', 'filter', '__texID')

    #textúra típus konstansok
    TEXTURE_DIFFUSE   = "diffuse"
    TEXTURE_BUMPMAP   = "bumpmap"
    TEXTURE_NORMALMAP = "normal"

    #Filter típus konstansok
    FILTER_NEAREST    = "nearest"
    FILTER_LINEAR     = "linear"
    FILTER_MIPMAP     = "mipmap"

    def __init__(self, src, filter="linear", type="diffuse"):
        """
        Textúra inicilaizálása

        @param  src:    A bitmap (bármely ismert képformátum) neve és elérési útja
        @type   src:    C{String}
        @param  filter: A textúra openGL filterezésének a típusa
        @type   filter: C{String}
        @param  type:   A textúra típusa
        @type   type:   C{String}
        """
        self.imageFile   = src                                                  #:@ivar: Textúra elérési útonala
        self.type        = type                                                 #:@ivar: Textúra típusa
        self.filter      = filter                                               #:@ivar: Textúra filter típusa
        self.__texID     = None                                                 #:@ivar: A texúra egyedi openGL azonosítója

        if self.type == Texture.TEXTURE_DIFFUSE:
            self.__genDiffuseMap()
        if self.type == Texture.TEXTURE_BUMPMAP:
            pass
        if self.type == Texture.TEXTURE_NORMALMAP:
            pass

    def bindTexture (self):
        """
        A textura kötése
        Az utóljára használt textúra lecserélése erre a textúrára. A rendszer a
        következtető textúra kötés beállíásig ezt használja
        """
        glBindTexture(GL_TEXTURE_2D, self.__texID)

    @classmethod
    def unbindTexture(self):
        """
        Textúra kötés megszüntetése
        """
        glBindTexture(GL_TEXTURE_2D,0)


    def __genDiffuseMap(self):
        """
        Alap textura
         1. Egydei openGL textúra azonosító generálása
         2. Képfájl betöltése
         3. Textúra filterezése
        """
        self.__texID = glGenTextures(1)
        self.__textureFilter(*self.__loadBitmap())


    def __loadBitmap(self):
        """
        Tetszőleges típusú képfájl betöltése a C{Python PIL} segítségével.
        A kép konvertálása RGBA formátumba

        @return:    A kép adatait, a kép szélessége és magassága
        @rtype:     C{Tuple}

        @see U{Python PIL 1.1.6 <http://www.pythonware.com/products/pil/>}
        """
        # létezik-e az elérési út és a fájl?
        if os.path.exists(self.imageFile) and os.path.isfile(self.imageFile):
            try:
                # kép betöltése
                img = imgOpen(self.imageFile, "r")
                try:
                    # a paettás képek RGB-re konvertálása
                    img = img.convert('RGB')
                    iw, ih, image = img.size[0], img.size[1], img.tostring("raw", "RGBA", 0, -1)
                except SystemError:
                    iw, ih, image = img.size[0], img.size[1], img.tostring("raw", "RGBX", 0, -1)

                assert iw * ih * 4 == len(image), """Nem megfelelő képméret! Támogatott formátumok: RGBX, RGBA"""
            except IOError as err:
                print "Bitmap betöltési hiba: ", err
        else:
            raise IOError("A képfájl nem található: " + imageFile)

        return image, iw, ih


    def __textureFilter (self, image, iw, ih):
        """
        openGL filter alkalmazása a betöltött képre
        Háromféle filterezés lehetséges:
         - közelitő C{nearest} filterezés
         - egyenletes C{linear} filterezés
         - C{mipmap} filterezés

        @param  image:  Kép adatok
        @type   image:  C{String}
        @param  iw:     Kép szélesség
        @type   iw:     C{int}
        @param  ih:     Kép magasság
        @type   ih:     C{int}
        """
        # nearest filterezés
        if self.filter == Texture.FILTER_NEAREST:
            glBindTexture(GL_TEXTURE_2D, self.__texID)
            glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, iw, ih, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
            return

        # linear filterezés
        if self.filter == Texture.FILTER_LINEAR:
            glBindTexture(GL_TEXTURE_2D, self.__texID)
            glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, iw, ih, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
            return

        # mipmap filterezés
        if self.filter == Texture.FILTER_MIPMAP:
            glTexParameteri(GL_TEXTURE_2D, GL_GENERATE_MIPMAP, GL_TRUE)
            glBindTexture(GL_TEXTURE_2D, self.__texID)

            glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

            glTexImage2D(GL_TEXTURE_2D, 0, 3, iw, ih, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
            return


    def remove(self):
        """
        A textúra törlése a memóriából
        """
        if self.__texID != None:
            glDeleteTextures([self.__texID])




class Shader():
    """
    Vertex és fragment shaderek kezelése.

    Főbb jellemzők:
     - Forrás betöltése
     - A forrás lefodítása
     - Shader program összeállítás
    """

    __slots__ = ('__v_src', '__f_src', '__shaders', '__program')

    def __init__(self, vertex_src = "", fragment_src = ""):
        """
        Shader programforrások beolvasása

        @param  vertex_src:     A Vertex Shader program forráskódja
        @type   vertex_src:     C{string}
        @param  fragment_src:   A Fragment Shader program forráskódja
        @type   fragment_src:   C{string}
        """
        self.__v_src   = vertex_src                                             #:@ivar: Vertex shader forráskód
        self.__f_src   = fragment_src                                           #:@ivar: Fragment shader forráskód
        self.__shaders = []                                                     #:@ivar: A lefordított vertex és fragment shaderek tárolója
        self.__program = None                                                   #:@ivar: Az összeállított shaderporgram

        self.__createShaderProgram()


    def bindShader(self):
        """
        Shaderek kötése
        Az utóljára használt sheder lecserélése erre a shaderre. A rendszer a
        következtető shader kötés beállíásig ezt használja
        """
        if self.__program != None:
            glUseProgram(self.__program)

    @classmethod
    def unbindShader(self):
        """
        Shader kötés megszüntetése
        """
        glUseProgram(0)


    def __createShaderProgram(self):
        """
        A megadott paraméterek ellenőrzése Shaderek fordítása és linkelése
        """
        if self.__v_src != "" or self.__f_src != "":
            self.__program = glCreateProgram()

            #Vertex shader fordítása és hozzáadása a shader programhoz
            if self.__v_src != "":
                v_shader = self.__compileShader(GL_VERTEX_SHADER, self.__v_src)
                self.__shaders.append(v_shader)
                glAttachShader(self.__program, v_shader)
                del self.__v_src

            #Fragment shader fordítása és hozzáadása a shader programhoz
            if self.__f_src != "":
                f_shader = self.__compileShader(GL_FRAGMENT_SHADER, self.__f_src)
                self.__shaders.append(f_shader)
                glAttachShader(self.__program, f_shader)
                del self.__f_src

            #Shader program linkelése
            glLinkProgram(self.__program)
        else:
            self.__program = None


    def __compileShader(self, type, src):
        """
        Shader fordítása és a fordítási státus ellenőrzése, továbbá a felmerülő
        hibák kezelése

        @param  type:   A fordítandó shader típusa
        @type   type:   C{GLuint}
        @param  src:    A shader forráskódja
        @type   src:    C{string}

        @todo:  A fordítási státusz lekérdezése nem működik, PyGL hiba
        """
        shader = glCreateShader(type)
        glShaderSource(shader, src)
        glCompileShader(shader)

        compileStatus = glGetShaderiv(shader, GL_COMPILE_STATUS)

        if not compileStatus:
            if glGetShaderiv(shader, GL_INFO_LOG_LENGTH) > 0:
                log = glGetShaderInfoLog(shader)
                print >> sys.stderr, log.value
            glDeleteShader(shader)
            raise IloError("Sikertelen Shader fordítás")

        return shader


    def remove(self):
        """
        Törli a shaderprogramot és a shadereket a memóriából
        """
        if self.__program != None:
            for shader in self.__shaders:
                glDetachShader(self.__program, shader)
                glDeleteShader(shader)
            glDeleteProgram(self.__program)
            del self.__shaders, self.__program

