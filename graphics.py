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
        #self.setMinimumSize(500, 500)
        self.setWindowState(self.windowState() | Qt.WindowFullScreen)
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
        # coordinates at beginning: (x,y)
        self.ballCoordinates = self.generateBallCoordinateList()
        self.powerupCoordinates = [(1,3), (26,3), (1,23), (26,23)]
        self.ghostCoordinates = [(13.5,11),(11.5,14),(13.5,14),(15.5,14)]
        self.characterCoordinate = (13.5,23)
        self.wallEdgeCoordinates = self.generateWallEdgeCoordinateList()
        self.ghostWallEdgeCoordinates = self.generateGhostWallEdgeCoordinateList()
        
        # items to draw
        self.food = [] # balls, powerups, fruit
        self.characters = [] # ghosts, character
        self.walls = [] # regular-, ghost-walls
    
    def generateBallCoordinateList(self):
        """
        rows and columns start at count 0
        and increase to the right and down
        Coordinates are stored as tuples:
        (x,y)
        x is column
        y is row
        """
        l=[]
        # x 6 & 21
        for i in range(2,27):
            l.append((6,i))
            l.append((21,i))
        # y 1
        for i in range(1,13):
            l.append((i,1))
        for i in range(15,27):
            l.append((i,1))
        # y 5 & 29
        for i in range(1,27):
            if i!=6 and i!=21:
                l.append((i,1))
            l.append((i,29))
        # y 8 & 26 & 20 & 23
        for i in range(1,27):
            if i not in [6,13,14,21]:
                l.append((i,20))
                if i not in [1,4,5,22,23,26]:
                    l.append((i,23))
                if i not in [7,8,19,20]:
                    l.append((i,8))
                    l.append((i,26))
        # y 2-4
        for i in range(2,5):
            if i!=3:
                l.append((1,i))
                l.append((26,i))
            l.append((12,i))
            l.append((15,i))
        # y 6 % 7
        for i in [1,9,18,26]:
            l.append((i,6))
            l.append((i,7))
        # y 21 &22
        for i in [1,12,15,26]:
            l.append((i,21))
            l.append((i,22))
        # y 24 & 25
        for i in [3,9,18,24]:
            l.append((i,24))
            l.append((i,25))
        # y 27 & 28
        for i in [1,12,15,26]:
            l.append((i,27))
            l.append((i,28))
        return l
    
    def generateWallEdgeCoordinateList(self):
        """
        rows and columns start at count 0
        and increase to the right and down
        Coordinates are stored as tuples:
        (x,y)
        x is column
        y is row
        """
        l=[]
        for i in range(0,28):
            # y 0 & 30
            l.append((i,0))
            l.append((i,30))
            if i not in [0,1,26,27]:
                # y 27 & 28
                if i not in [12,15]:
                    l.append((i,27))
                    l.append((i,28))
                
                if i not in [6,21]:
                    # y 2-4
                    if i not in [12,15]:
                        l.append((i,2))
                        l.append((i,4))
                        if i not in [3,4,8,9,10,17,18,19,23,24]:
                            l.append((i,3))
                    # y 6 & 7
                    if i not in [9,18]:
                        l.append((i,6))
                        l.append((i,7))
                    # y 21 & 22
                    if i not in [12,15]:
                        l.append((i,21))
                        l.append((i,22))
            # y 9 & 13 & 15 & 19 & 24 & 25
            if i not in [0,6,21,27]:
                if i not in [12,15]:
                    l.append((i,9))
                if i not in range(9,19):
                    l.append((i,13))
                    l.append((i,15))
                if i not in [9,18]:
                    l.append((i,19))
                    if i not in [3,24]:
                        l.append((i,24))
                        l.append((i,25))
        # x 0 & 27
        for i in range(1,30):
            if i not in [10,11,12,14,16,17,18]:
                l.append((0,i))
                l.append((27,i))
        # y 10 & 18
        for i in range(5,23):
            if i not in [6,21]:
                if i not in [12,15]:
                    l.append((i,10))
                if i not in [9,18]:
                    l.append((i,18))
        # y 1 & 20
        for i in [1,20]:
            l.append((13,i))
            l.append((14,i))
        # y 11 & 12 & 16 & 17
        for i in [11,12,16,17]:
            for j in [5,7,8,19,20,22]:
                l.append((j,i))
        # y 8 & 26
        for i in [7,8,13,14,19,20]:
            l.append((i,8))
            l.append((i,26))
        # y 23
        for i in [4,5,22,23]:
            l.append((i,23))
        return l
    
    def generateGhostWallEdgeCoordinateList(self):
        """
        rows and columns start at count 0
        and increase to the right and down
        Coordinates are stored as tuples:
        (x,y)
        x is column
        y is row
        """
        l=[]
        for i in range(10,18):
            l.append((i,12))
            l.append((i,16))
        for i in [13,14,15]:
            l.append((10,i))
            l.append((17,i))
        return l

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