# -*- coding: utf -*-

__author__="Vadasz Laszlo"
__date__ ="2009.08.27. 16:33:40"

from ilo.messages.events import *
from PyQt4 import QtGui

"""
A grafikus felhasználó felület alapelemeit tartalmazó modul
"""


class MainWindow(QtGui.QMainWindow):
    """
    Ilo ablak osztály

    Inicializálja a főablakot és tovább küldi a motornak a főbb eseményeket a
    belső eseménykezelőn keresztül.
    """

    __slots__ = ('disp', )

    def __init__(self, * args):
        """
        Az örökített QMainWindow és az esemény kezelő inicilalizálása
        """
        apply(QtGui.QMainWindow.__init__, (self,) + args)
        self.disp = EventDispatcher()                                           #:@ivar: Eseménydobó objektum


    def setGLContext(self, context):
        """
        Az ablak tartalmának beéllítaása.
        Ezzel kötjük össze a főablakot az OpenGL környezettel
        """
        self.setCentralWidget(context)


    def keyPressEvent (self, event):
        """
        Gomblenyomás esemény tovább küldése a belső esemény rendszerrel
        """
        self.disp.dispatchEvent(KeyboardEvent(KeyboardEvent.PRESS,
                                event.key(),
                                False,
                                False,
                                False))


    def keyReleaseEvent(self, event):
        """
        Gombfelengedés esemény tovább küldése a belső esemény rendszerrel
        """
        self.disp.dispatchEvent(KeyboardEvent(KeyboardEvent.RELEASE,
                                event.key(),
                                False,
                                False,
                                False))
