# -*- coding: utf -*-

__author__="Vadasz Laszlo"
__date__ ="2009.09.17. 9:17:22"

import os

from PyQt4 import QtGui, QtCore

class GameGui():
    def __init__(self, window):
        self.window = window
        apply(QtGui.QMainWindow.__init__, (self,) + args)
        #self.mainTimeLine = TimeLine(60)

        fileExit = QtGui.QAction(QtGui.QIcon('data/gui/icons/exit.png'), 'Exit', self)
        fileExit.setShortcut('Ctrl+Q')
        fileExit.setStatusTip('Exit application')
        self.window.connect(fileExit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))

        fileNew = QtGui.QAction(QtGui.QIcon('data/gui/icons/new_file.png'), '&New...', self)
        fileNew.setShortcut('Ctrl+N')
        fileNew.setStatusTip('Open map file')

        fileOpen = QtGui.QAction(QtGui.QIcon('data/gui/icons/open_file.png'), '&Open...', self)
        fileOpen.setShortcut('Ctrl+O')
        fileOpen.setStatusTip('Open map file')
        self.window.connect(fileOpen, QtCore.SIGNAL('triggered()'), self.showOpenDialog)

        fileSave = QtGui.QAction(QtGui.QIcon('data/gui/icons/save_file.png'), '&Save...', self)
        fileSave.setShortcut('Ctrl+S')
        fileSave.setStatusTip('Save map file')
        self.window.connect(fileSave, QtCore.SIGNAL('triggered()'), self.showSaveDialog)

        fileSaveas = QtGui.QAction(QtGui.QIcon('data/gui/icons/save_as_file.png'), '&Save as...', self)
        fileSaveas.setShortcut('Ctrl+Shift+S')
        fileSaveas.setStatusTip('Save as map file')
        self.window.connect(fileSaveas, QtCore.SIGNAL('triggered()'), self.showSaveDialog)

        viewFullScr = QtGui.QAction(QtGui.QIcon('data/gui/icons/fullscreen.png'), '&Fullscreen', self)
        viewFullScr.setShortcut('F11')
        viewFullScr.setStatusTip('Toogle Fullscreen')
        viewFullScr.setCheckable(True)
        def toggleScr():
            if viewFullScr.isChecked():
                self.toggleScreenMode("full")
            else:
                self.toggleScreenMode("normal")
        self.window.connect(viewFullScr, QtCore.SIGNAL('triggered()'), toggleScr)


        helpAbout = QtGui.QAction(QtGui.QIcon('data/gui/icons/about.png'), 'About', self)
        helpAbout.setStatusTip('About application')
        self.window.connect(helpAbout, QtCore.SIGNAL('triggered()'), self.showAboutDialog)

        helpAboutQt = QtGui.QAction(QtGui.QIcon('data/gui/icons/aboutqt.png'), 'About Qt', self)
        helpAboutQt.setStatusTip('About Qt')
        self.window.connect(helpAboutQt, QtCore.SIGNAL('triggered()'), self.showAboutQtDialog)

        self.window.statusBar()

        menubar = self.menuBar()
        file = menubar.addMenu('&File')
        file.addAction(fileNew)
        file.addAction(fileOpen)
        file.addAction(fileSave)
        file.addAction(fileSaveas)
        file.addSeparator()
        file.addAction(fileExit)

        edit = menubar.addMenu('&Edit')

        view = menubar.addMenu('&View')
        for res in [["640x480", self.setScreenSize640x480], ["800x600", self.setScreenSize800x600], ["1024x768", self.setScreenSize1024x768]]:
            act = QtGui.QAction( res[0], self)
            act.setStatusTip('Set screen size ' + res[0])
            self.window.connect(act, QtCore.SIGNAL('triggered()'), res[1])
            view.addAction(act)
        view.addSeparator()
        view.addAction(viewFullScr)

        tools = menubar.addMenu('&Tools')

        help = menubar.addMenu('&Help')
        help.addAction(helpAbout )
        help.addAction(helpAboutQt )


        toolbar = self.window.addToolBar('File')
        toolbar.addAction(fileNew)
        toolbar.addAction(fileOpen)
        toolbar.addAction(fileSave)
        toolbar.hide()

    def showOpenDialog(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open file','/')
        self.setWindowTitle("Ilo engine - " + filename.split("/")[-1])
        self.__engine.loadMap(filename)

    def showSaveDialog(self):
        filename = QtGui.QFileDialog.getSaveFileName(self, 'Save file','/')

    def showAboutDialog(self):
        QtGui.QMessageBox.about(self,"About Ilo Engine", "Ilo Engine\nVersion: 0.1")

    def showAboutQtDialog(self):
        QtGui.QMessageBox.aboutQt(self, "Ilo")

    def setScreenSize640x480 (self):
        self.setScreenSize(640, 480)

    def setScreenSize800x600 (self):
        self.setScreenSize(800, 600)

    def setScreenSize1024x768 (self):
        self.setScreenSize(1024, 768)

    def setScreenSize(self, w, h):
        self.setFixedSize(w, h)

    def toggleScreenMode(self, mode):
        if mode == "full":
            self.showFullScreen()

        elif mode == "normal":
            self.showNormal()


    def setOSScreenSize(self, w, h, bits = 32, frec = "60"):
        sistem=os.name
        if sistem=="nt":
            import win32api
            import win32con
            import pywintypes

            self.display_modes = {}
            n = 0
            while True:
                try:
                    devmode = win32api.EnumDisplaySettings (None, n)
                except pywintypes.error:
                    break
                else:
                    key = (
                        devmode.BitsPerPel,
                        devmode.PelsWidth,
                        devmode.PelsHeight,
                        devmode.DisplayFrequency
                    )
                    display_modes[key] = devmode
                    n += 1

            mode_required = (bits, w, h, frec)
            try:
                devmode = display_modes[mode_required]
            except KeyError:
                print "This resolution: " + mode_required + " not avalible"
            else:
                win32api.ChangeDisplaySettings (devmode, 0)

        elif sistem=="posix":
            os.system("xrandr -s 1280x800")
        else:
            # Apple OSX
            pass