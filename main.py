"""
    Pacman Clone
    by Miitcher
    For fun project doing a Pacman clone.
    
    Python 3.4
    PySide #
"""

from graphics import *
from ui import Settings, KeyHandler

import sys
from PySide.QtGui import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.keyHandler = KeyHandler(self)
        self.setWindowTitle("Packman Clone")
    
    def setupWindow(self, settings):
        self.settings = settings
        self.getSettings()
        self.resize(round(self.width*self.menuScale), round(self.height*self.menuScale))
        # set MainWindow to center
        self.toMenuW()
    
    def getSettings(self):
        (self.width, self.height) = self.settings.getResolution()
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
        self.GameW.update()
        self.setCentralWidget(self.GameW)
    
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
    mainWindow.setupWindow(settings)
    # TESTING
    mainWindow.toGameW()
    #sys.exit()
    # TESTING
    mainWindow.show()
    sys.exit(app.exec_())