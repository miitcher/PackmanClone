"""
    Handles graphics.
    https://wiki.qt.io/PySideDocumentation
    
    Design:
        black background
        hollow dark blue walls
        balls solid yellow
        powerup balls are pink
        character solid yellow
        ghosts have mooving eyes
            are colours: red, cyan, pink and orange
"""

import sys
from PySide.QtCore import *
from PySide.QtGui import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupWindow()
        self.goToMenuW()
    
    def setupWindow(self):
        self.setCursor(Qt.ArrowCursor)
        self.setWindowTitle("Packman Clone")
        self.setMinimumSize(500, 500)
        """
        screenGeometry = QApplication.desktop().screenGeometry()
        self.screenWidth = screenGeometry.width()
        self.screenHeight = screenGeometry.height()
        """
    
    def goToMenuW(self):
        self.setCursor(Qt.ArrowCursor)
        self.menuW = MenuW(self)
        self.setCentralWidget(self.menuW)
    
    def goToGameW(self):
        self.setCursor(Qt.BlankCursor)
        self.GameW = GameW(self)
        self.setCentralWidget(self.GameW)
    
    def goToHighscoresW(self):
        self.setCursor(Qt.ArrowCursor)
        self.HighscoresW = HighscoresW(self)
        self.setCentralWidget(self.HighscoresW)

class OwnW(QWidget):
    def __init__(self, MWindow):
        super().__init__()
        self.MWindow = MWindow
    
    def setupWidget(self):
        # method defined in child
        pass

class MenuW(OwnW):
    def __init__(self, MWindow):
        super().__init__(MWindow)
    
    def setupWidget(self):
        pass

class GameW(QWidget):
    def __init__(self, MWindow):
        super().__init__(MWindow)
    
    def setupWidget(self):
        pass

class HighscoresW(QWidget):
    def __init__(self, MWindow):
        super().__init__(MWindow)
    
    def setupWidget(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())