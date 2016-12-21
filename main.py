"""
    Pacman Clone
    by Miitcher
    For fun project doing a Pacman clone.
    
    Python 3.4
    PySide #
"""

from graphics import *
from ui import Settings, KeyHandler
from physics import Physics

import sys
from PySide.QtGui import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Packman Clone")
    
    def setupWindow(self, settings, physics):
        self.keyHandler = KeyHandler()
        self.settings = settings
        self.physics = physics
        self.getSettings()
        self.calculateCorScale()
        self.settings.setVariables(self.corScale)
        self.physics.setupPhysics(self.fps)
        
        self.resize(round(self.width*self.menuScale), round(self.height*self.menuScale))
        # set MainWindow to center
        self.toMenuW()
    
    def getSettings(self):
        (self.width, self.height) = self.settings.getResolution()
        self.fps = self.settings.getFPS()
        self.menuScale = self.settings.getMenuScale()
        self.windowMode = self.settings.getWindowMode()
    
    def calculateCorScale(self):
        """
        "corScale" is the ratio between the pixel- and 
        general coordinates (corScale = PixelCor / GeneralCor).
        
        The GeneralCor game-areas coordinate ranges are:
            x: [0, 27], y: [0, 30]
        We give extra space, in GeneralCor units:
            right/left: 1, up: 3, down: 2
        Extra spaces combined is:
            horisontal: 2, vertical: 5
        Now our GeneralCor side lenghts are:
            x: 29, y: 35
        The extra space up and left need buffers.
        """
        self.CorOffset = (1,3)
        xLenGCor = 29   # 27 + 2
        yLenGCor = 35   # 30 + 5
        xRatio = self.width  / xLenGCor
        yRatio = self.height / yLenGCor
        # We determine the conversion between GCor
        # and PCor with the limiting length.
        if xRatio > yRatio:
            # height (y) limits
            self.corScale = yRatio
        else:
            # width (x) limits
            self.corScale = xRatio
        
        self.gameAreaSize = (self.corScale * xLenGCor, self.corScale * yLenGCor)
    
    def keyPressEvent(self, e):
        if e.isAutoRepeat():
            e.ignore()
            return
        self.keyHandler.keyPressed(self.centralWidget(), e)
    
    def toMenuW(self):
        self.setCursor(Qt.ArrowCursor)
        self.menuW = MenuW(self)
        self.menuW.setupWidget()
        self.setCentralWidget(self.menuW)
    
    def toGameW(self):
        #self.setCursor(Qt.BlankCursor)
        self.GameW = GameW(self)
        self.GameW.setupWidget()
        if self.windowMode == "Fullscreen":
            self.resize(self.width, self.height)
            # should be real fullscreen
            # self.MWindow.windowMode
        elif self.windowMode == "Windowed":
            self.resize(self.gameAreaSize[0], self.gameAreaSize[1])
        self.setCentralWidget(self.GameW)
        self.GameW.startGame()
    
    def toSettingsW(self):
        self.setCursor(Qt.ArrowCursor)
        self.SettingsW = SettingsW(self)
        self.SettingsW.setupWidget()
        self.setCentralWidget(self.SettingsW)
    
    def toHighscoresW(self):
        self.setCursor(Qt.ArrowCursor)
        self.HighscoresW = HighscoresW(self)
        self.HighscoresW.setupWidget()
        self.setCentralWidget(self.HighscoresW)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    settings = Settings()
    physics = Physics()
    mainWindow.setupWindow(settings, physics)
    # TESTING
    mainWindow.toGameW()
    #sys.exit()
    # TESTING
    mainWindow.show()
    sys.exit(app.exec_())