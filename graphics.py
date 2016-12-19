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

from ui import Settings
from bodies import *

import sys
from PySide.QtCore import *
from PySide.QtGui import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Packman Clone")
        #TODO: find minimum size
        #self.setMinimumSize(500, 500)
    
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


class OwnW(QWidget):
    def __init__(self, MWindow):
        super().__init__()
        self.MWindow = MWindow
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)

class MenuW(OwnW):
    def __init__(self, MWindow):
        super().__init__(MWindow)
    
    def setupWidget(self):
        StartGameButton = QPushButton("START GAME")
        SettingsButton = QPushButton("SETTINGS")
        HighscoresButton = QPushButton("HIGHSCORES")
        
        StartGameButton.clicked.connect(self.MWindow.toGameW)
        SettingsButton.clicked.connect(self.MWindow.toSettingsW)
        HighscoresButton.clicked.connect(self.MWindow.toHighscoresW)
        
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(StartGameButton)
        vbox.addWidget(SettingsButton)
        vbox.addWidget(HighscoresButton)
        vbox.addStretch(1)
        
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addLayout(vbox)
        hbox.addStretch(1)
        
        self.setLayout(hbox)

class GameW(OwnW):
    def __init__(self, MWindow):
        super().__init__(MWindow)
    
    def setupWidget(self):
        """
        There are generel coordinates and pixel coordinates.
        These coordinates will be called "GCor" and "PCor".
        Both have their origo in the screens upper-left-corner,
        and the horisontal (width) measure is x,
        and the vertical (height) is y as: "(x,y)".
        """
        self.generateGCors()
        self.makePCorsFromGCors()
        self.setupBodies()
        self.setBodyCoordinates()
        print("GameW set")
    
    def setMWSize(self):
        self.MWindow.resize(self.gameAreaSize[0], self.gameAreaSize[1])
    
    def paintEvent(self, e):
        painter = QPainter()
        painter.begin(self)
        
        for b in self.BODYLIST:
            b.draw(painter)
        
        painter.end()
    
    def generateGCors(self):
        self.pacmanGCor = [(13.5,23)]
        self.fruitGCor = [(13.5,17)]
        self.ghostGCors = [(13.5,11),(11.5,14),(13.5,14),(15.5,14)]
        self.wallEdgeGCors = self.generateWallEdgeGCoordinateList()
        self.ghostWallEdgeGCors = self.generateGhostWallEdgeGCoordinateList()
        self.ballGCors = self.generateBallGCoordinateList()
        self.powerupGCors = [(1,3), (26,3), (1,23), (26,23)]
    
    def makePCorsFromGCors(self):
        """
        The GCor game-areas coordinate ranges are:
            x: [0, 27], y: [0, 30]
        We give extra space, in GCor units:
            right/left: 1, up: 3, down: 2
        Extra spaces combined is:
            horisontal: 2, vertical: 5
        Now our GCor side lenghts are:
            x: 29, y: 35
        The extra space up and left need buffers.
        """
        self.xBufferGCor = 1
        self.yBufferGCor = 3
        xLenGCor = 29
        yLenGCor = 35
        xRatio = self.MWindow.width  / xLenGCor
        yRatio = self.MWindow.height / yLenGCor
        # We determine the conversion between GCor
        # and PCor with the limiting length.
        if xRatio > yRatio:
            # height (y) limits
            self.PToG = yRatio
        else:
            # width (x) limits
            self.PToG = xRatio
        
        self.gameAreaSize = (self.PToG * xLenGCor, self.PToG * yLenGCor)
        
        self.pacmanPCor         = self.modifyTuppleList(self.pacmanGCor)
        self.fruitPCor          = self.modifyTuppleList(self.fruitGCor)
        self.ghostPCors         = self.modifyTuppleList(self.ghostGCors)
        self.wallEdgePCors      = self.modifyTuppleList(self.wallEdgeGCors)
        self.ghostWallEdgePCors = self.modifyTuppleList(self.ghostWallEdgeGCors)
        self.ballPCors          = self.modifyTuppleList(self.ballGCors)
        self.powerupPCors       = self.modifyTuppleList(self.powerupGCors)
    
    def modifyTuppleList(self, list):
        newList = []
        for tupple in list:
            newList.append(( self.PToG * (self.xBufferGCor + tupple[0]),
                             self.PToG * (self.yBufferGCor + tupple[1]) ))
        return(newList)
    
    def setupBodies(self):
        self.pacmanList = [Pacman(self)]
        self.fruitList = [Fruit(self)]
        self.ghostList = setupGhostList(self)
        self.wallList = setupWallList(self)
        self.ghostWallList = setupGhostWallList(self)
        self.ballList = setupBallList(self)
        self.powerupList = setupPowerupList(self)
        self.addBodiesToBODYLIST() # self.BODYLIST
    
    def addBodiesToBODYLIST(self):
        self.BODYLIST = []
        self.addListToBodyList(self.pacmanList)
        self.addListToBodyList(self.fruitList)
        self.addListToBodyList(self.ghostList)
        self.addListToBodyList(self.wallList)
        self.addListToBodyList(self.ghostWallList)
        self.addListToBodyList(self.ballList)
        self.addListToBodyList(self.powerupList)
    
    def addListToBodyList(self, sourceList):
        for i in sourceList:
            self.BODYLIST.append(i)
    
    def setBodyCoordinates(self):
        self.setCoordinatesForAList(self.pacmanList, self.pacmanPCor)
        self.setCoordinatesForAList(self.fruitList, self.fruitPCor)
        self.setCoordinatesForAList(self.ghostList, self.ghostPCors)
        self.setCoordinatesForAList(self.wallList, self.wallEdgePCors)
        self.setCoordinatesForAList(self.ghostWallList, self.ghostWallEdgePCors)
        self.setCoordinatesForAList(self.ballList, self.ballPCors)
        self.setCoordinatesForAList(self.powerupList, self.powerupPCors)
    
    def setCoordinatesForAList(self, bodyList, corList):
        for i in range(len(corList)):
            bodyList[i].setStartCoordinateAndScale(corList[i], self.PToG)
            bodyList[i].moveToStart()
    
    def generateBallGCoordinateList(self):
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
        
        for i in range(1,27):
            # y 1
            if i not in [13,14]:
                l.append((i,1))
            # y 5 & 29
            if i not in [6,21]:
                l.append((i,5))
            l.append((i,29))
            # y 8 & 26 & 20 & 23
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
    
    def generateWallEdgeGCoordinateList(self):
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
    
    def generateGhostWallEdgeGCoordinateList(self):
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

class SettingsW(OwnW):
    def __init__(self, MWindow):
        super().__init__(MWindow)
    
    def setupWidget(self):
        pass

class HighscoresW(OwnW):
    def __init__(self, MWindow):
        super().__init__(MWindow)
    
    def setupWidget(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())