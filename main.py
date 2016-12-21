"""
    Pacman Clone
    by Miitcher
    For fun project doing a Pacman clone.
    
    Python 3.4
    PySide #
"""

from graphics import *
from ui import Settings, KeyHandler

import sys, os, shutil
from PySide.QtGui import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Packman Clone")
        
        self.keyHandler = KeyHandler()
        self.settings = Settings()
        self.processSettingsChanged()
        
        # set MainWindow to center
        self.toMenuW()
    
    def processSettingsChanged(self):
        #Called when settings changed.
        #self.getSettingValues()
        self.calculateCorScaleAndCorOffset()
        self.settings.setVariables(self.corScale)
    """
    def getSettingValues(self):
        (self.width, self.height) = self.settings.getResolution()
        self.fps = self.settings.getFPS()
        self.menuScale = self.settings.getMenuScale()
        self.windowMode = self.settings.getWindowMode()
    """
    def calculateCorScaleAndCorOffset(self):
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
        self.corOffset = (1,3)
        xLenGCor = 29   # 27 + 2
        yLenGCor = 35   # 30 + 5
        xRatio = self.settings.width  / xLenGCor
        yRatio = self.settings.height / yLenGCor
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
        self.resize(round(self.settings.width*self.settings.menuScale),
                    round(self.settings.height*self.settings.menuScale))
        self.setCursor(Qt.ArrowCursor)
        self.menuW = MenuW(self)
        self.menuW.setupWidget()
        self.setCentralWidget(self.menuW)
    
    def toGameW(self):
        #self.setCursor(Qt.BlankCursor)
        self.GameW = GameW(self)
        self.GameW.setupWidget()
        if self.settings.windowMode == "Fullscreen":
            self.resize(self.width, self.height)
            # should be real fullscreen
            # self.MWindow.windowMode
        elif self.settings.windowMode == "Windowed":
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

def handleBackup():
    """
    If there is a bacaup of the settings-file
    it will be turned into the used settings-file.
    """
    if os.path.isfile("settings_BACKUP.ini"):
        shutil.copyfile("settings_BACKUP.ini", "settings.ini")
        os.remove("settings_BACKUP.ini")
        print('Made "settings_BACKUP.ini" to the "settings.ini".')
    

if __name__ == '__main__':
    handleBackup()
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    # TESTING
    mainWindow.toGameW()
    #sys.exit()
    # TESTING
    mainWindow.show()
    sys.exit(app.exec_())