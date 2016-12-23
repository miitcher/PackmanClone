"""
    Pacman Clone
    by Miitcher
    For fun project doing a Pacman clone.
    
    Python 3.4
    PySide #
    
    TODO:
        Write more tests.
        Make better drawn walls.
        Make better ghost drawing (propably static images).
        Implement ghost AI (could be just random).
        Implement collision detection.
        
        Implement highscores.
        Implement settings menu.
        Add sounds.
        Work on menus.
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
        
        # set MainWindow to center
        self.toMenuW()
    
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
            self.resize(self.settings.width, self.settings.height)
            # should be real fullscreen
            # self.MWindow.windowMode
        elif self.settings.windowMode == "Windowed":
            self.resize(self.settings.gameAreaSize[0],
                        self.settings.gameAreaSize[1])
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