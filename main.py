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
        self.keyHandler = KeyHandler(self)
        self.setWindowTitle("Packman Clone")
    
    def setupWindow(self, settings, physics):
        self.settings = settings
        self.physics = physics
        self.getSettings()
        self.physics.setRefresh(self.fps)
        
        self.resize(round(self.width*self.menuScale), round(self.height*self.menuScale))
        # set MainWindow to center
        self.toMenuW()
    
    def getSettings(self):
        (self.width, self.height) = self.settings.getResolution()
        self.fps = self.settings.getFPS()
        self.menuScale = self.settings.getMenuScale()
        self.windowMode = self.settings.getWindowMode()
    
    def keyPressEvent(self, e):
        if e.isAutoRepeat():
            e.ignore()
            return
        self.keyHandler.keyPressed(self.centralWidget(), e)
    
    def keyReleaseEvent(self, e):
        self.keyHandler.keyReleased(e)
    
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
            self.GameW.setMWSize()
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