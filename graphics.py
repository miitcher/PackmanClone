"""
    Handles graphics.
    https://wiki.qt.io/PySideDocumentation
    https://deptinfo-ensip.univ-poitiers.fr/ENS/pyside-docs/index.html
    
    Design:
        black background
        hollow dark blue walls
        balls solid yellow
        powerup balls are pink
        character solid yellow
        ghosts have mooving eyes
            are colours: red, cyan, pink and orange
"""

from bodies import *

from PySide.QtCore import *
from PySide.QtGui import *


class OwnW(QWidget):
    def __init__(self, MWindow):
        super().__init__()
        self.MWindow = MWindow
        self.settings = MWindow.settings
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)

class MenuW(OwnW):
    def __init__(self, MWindow):
        super().__init__(MWindow)
    
    def __str__(self):
        return "MenuW"
    
    def setupWidget(self):
        StartGameButton = QPushButton("START GAME")
        SettingsButton = QPushButton("SETTINGS")
        HighscoresButton = QPushButton("HIGHSCORES")
        
        StartGameButton.clicked.connect(self.MWindow.toGameW)
        SettingsButton.clicked.connect(self.MWindow.toSettingsW)
        HighscoresButton.clicked.connect(self.MWindow.toHighscoresW)
        """
        Show the usable widgets.
        """
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(StartGameButton)
        #vbox.addWidget(SettingsButton)
        #vbox.addWidget(HighscoresButton)
        vbox.addStretch(1)
        
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addLayout(vbox)
        hbox.addStretch(1)
        
        self.setLayout(hbox)

class GameW(OwnW):
    def __init__(self, MWindow):
        super().__init__(MWindow)
        self.keyHandler = MWindow.keyHandler
    
    def __str__(self):
        return "GameW"
    
    def startGame(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.timerEventFPS)
        self.timer.start(1000/self.settings.fps) # [ms]
        
        self.timerG = QTimer()
        self.timerG.timeout.connect(self.timerEventGFPS)
        self.timerG.start(1000/self.settings.gfps) # [ms]
        
        print("fps & gfps:",self.settings.fps, self.settings.gfps)
    
    def timerEventFPS(self):
        self.update()
    
    def timerEventGFPS(self):
        self.pacmanList[0].process()
    
    def setupWidget(self):
        """
        There are generel coordinates and pixel coordinates.
        These coordinates will be called "GCor" and "PCor".
        Both have their origo in the screens upper-left-corner,
        and the horisontal (width) measure is x,
        and the vertical (height) is y as: "(x,y)".
        """
        self.generateCoordinates()
        self.modifyCoordinateLists()
        self.settings.movementMatrix = self.movementMatrix
        self.createBodies()
        print("GameW set")
    
    def setupPhysicsForBodies(self):
        pass
    
    def paintEvent(self, e):
        painter = QPainter()
        painter.begin(self)
        
        self.drawBodyList(self.fruitList, painter)
        self.drawBodyList(self.powerupList, painter)
        self.drawBodyList(self.ballList, painter)
        self.drawBodyList(self.ghostList, painter)
        self.drawBodyList(self.pacmanList, painter)
        
        # remove wall items (they slow things down
        self.drawBodyList(self.ghostWallList, painter)
        self.drawBodyList(self.wallList, painter)
        
        #self.drawMowementMatrix(painter) # Debug
        
        painter.end()
    
    def drawMowementMatrix(self, painter):
        # For debug purposes.
        painter.setPen(QPen())
        k = self.settings.corScale
        (xOffset, yOffset) = self.settings.corOffset
        x = len(self.movementMatrix)
        y = len(self.movementMatrix[0])
        size = k/4
        for i in range(x):
            for j in range(y):
                value = self.movementMatrix[i][j]
                if value in [1,2]:
                    if value == 1:
                        colour = Qt.green
                    else:
                        colour = Qt.gray
                    painter.setBrush(colour)
                    painter.drawRect(k*(i + xOffset), k*(j + yOffset), size, size)
    
    def drawBodyList(self, bodyList, painter):
        for b in bodyList:
            b.draw(painter)
    
    def generateCoordinates(self):
        self.pacmanCor = [(13.5,23)]
        self.fruitCor = [(13.5,17)]
        self.ghostCors = [(13.5,11),(11.5,14),(13.5,14),(15.5,14)]
        self.wallEdgeCors = self.generateWallEdgeGCoordinateList()
        self.ghostWallEdgeCors = self.generateGhostWallEdgeGCoordinateList()
        self.ballCors = self.generateBallGCoordinateList()
        self.powerupCors = [(1,3), (26,3), (1,23), (26,23)]
        self.movementMatrix = self.generateMovementMatrix()
    
    @staticmethod
    def generateWallEdgeGCoordinateList():
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
    
    @staticmethod
    def generateGhostWallEdgeGCoordinateList():
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
    
    @staticmethod
    def generateBallGCoordinateList():
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
    
    def generateMovementMatrix(self):
        """
        The movementMatrix determine witch nodes can be moved trough.
        You can move between two nodes if they are next to eachother
        verticaly or horisontaly.
        A node of value 1 is accessible to pacman and ghosts.
        A node of value 2 is accessible to just ghosts.
        A node of value 0 is not accessible.
        The movementMatrix is accessed like: m[x][y]
        The ranges are:
            x: [0, 27], y: [0, 29]
        We need buffers on the right and the bottom of
        the game area, therefore we add one node to
        the x and y lengths.
        """
        m = []
        for x in range(29):
            m.append([0] * 31)
        
        # We lists to set the movementMatrix.
        self.placeValueInMatrixOnListCoordinates(1, m, self.ballCors)
        self.placeValueInMatrixOnListCoordinates(1, m, self.powerupCors)
        
        emptyAccessibleCors = [(12,9),(15,9),(12,10),(15,10),(13,23),(14,23)]
        for i in range(28):
            if i not in [6,21] and i not in range(9,19):
                emptyAccessibleCors.append((i,14))
        for i in range(10,18):
            emptyAccessibleCors.append((i,11))
            emptyAccessibleCors.append((i,17))
        for j in range(11,20):
            emptyAccessibleCors.append((9,j))
            emptyAccessibleCors.append((18,j))
        self.placeValueInMatrixOnListCoordinates(1, m, emptyAccessibleCors)
        
        corsAccessibleToGhosts = [(13,12),(14,12)]
        for i in range(11,17):
            for j in range(13,16):
                corsAccessibleToGhosts.append((i,j))
        self.placeValueInMatrixOnListCoordinates(2, m, corsAccessibleToGhosts)
        
        return(m)
    
    @staticmethod
    def placeValueInMatrixOnListCoordinates(value, matrix, corList):
        for corTupple in corList:
            matrix[corTupple[0]][corTupple[1]] = value
    
    
    def modifyCoordinateLists(self):
        self.pacmanCor         = self.modifyTuppleList(self.pacmanCor)
        self.fruitCor          = self.modifyTuppleList(self.fruitCor)
        self.ghostCors         = self.modifyTuppleList(self.ghostCors)
        self.wallEdgeCors      = self.modifyTuppleList(self.wallEdgeCors)
        self.ghostWallEdgeCors = self.modifyTuppleList(self.ghostWallEdgeCors)
        self.ballCors          = self.modifyTuppleList(self.ballCors)
        self.powerupCors       = self.modifyTuppleList(self.powerupCors)
    
    def modifyTuppleList(self, list):
        newList = []
        [xOffset, yOffset] = self.settings.corOffset
        k = self.settings.corScale
        for tupple in list:
            # The buffers are; x:1, y:3
            newList.append(( k * (xOffset + tupple[0]),
                             k * (yOffset + tupple[1]) ))
        return(newList)
    
    
    def createBodies(self):
        self.pacmanList     = self.createBodyListFromCorList("Pacman", self.pacmanCor)
        self.fruitList      = self.createBodyListFromCorList("Fruit", self.fruitCor)
        self.ghostList      = self.createBodyListFromCorList("Ghost", self.ghostCors)
        i = 0
        for ghost in self.ghostList:
            ghost.setGhostIndex(i)
            i += 1
        self.wallList       = self.createBodyListFromCorList("Wall", self.wallEdgeCors)
        self.ghostWallList  = self.createBodyListFromCorList("GhostWall", self.ghostWallEdgeCors)
        self.ballList       = self.createBodyListFromCorList("Ball", self.ballCors)
        self.powerupList    = self.createBodyListFromCorList("Powerup", self.powerupCors)
    
    def createBodyListFromCorList(self, BodyClass, CorList):
        list = []
        for cor in CorList:
            bodyInput = [cor, self.settings]
            if BodyClass == "Pacman":
                bodyInput = [cor, self.settings, self.keyHandler]
                list.append(Pacman(bodyInput))
            elif BodyClass == "Fruit":
                list.append(Fruit(bodyInput))
            elif BodyClass == "Ghost":
                list.append(Ghost(bodyInput))
            elif BodyClass == "Wall":
                list.append(Wall(bodyInput))
            elif BodyClass == "GhostWall":
                list.append(GhostWall(bodyInput))
            elif BodyClass == "Ball":
                list.append(Ball(bodyInput))
            elif BodyClass == "Powerup":
                list.append(Powerup(bodyInput))
        return list

class SettingsW(OwnW):
    def __init__(self, MWindow):
        super().__init__(MWindow)
    
    def __str__(self):
        return "SettingsW"
    
    def setupWidget(self):
        pass

class HighscoresW(OwnW):
    def __init__(self, MWindow):
        super().__init__(MWindow)
    
    def __str__(self):
        return "HighscoresW"
    
    def setupWidget(self):
        pass
