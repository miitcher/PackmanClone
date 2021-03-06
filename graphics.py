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
        self.backgroundImage = QPixmap("files/game_backgroung.png")
        self.paused = False
    
    def __str__(self):
        return "GameW"
    
    def startGame(self):
        self.timerFPS = QTimer()
        self.timerFPS.timeout.connect(self.timerEventFPS)
        self.timerFPS.start(1000/self.settings.fps) # [ms]
        
        self.timerGame = QTimer()
        self.timerGame.timeout.connect(self.timerEventGameFPS)
        self.timerGame.start(1000/self.settings.gfps) # [ms]
        
        self.timerGhost = QTimer()
        self.timerGhost.timeout.connect(self.timerEventGhost)
        self.timerGhost.start(1000*self.settings.ghostSpawnIntervall)
    
    def pauseOrUnpauseGame(self):
        # pauses or unpauses the timers
        if self.paused:
            self.timerFPS.start()
            self.timerGame.start()
            self.timerGhost.start()
            self.paused = False
        else:
            self.timerFPS.stop()
            self.timerGame.stop()
            self.timerGhost.stop()
            self.paused = True
    
    def timerEventFPS(self):
        self.update()
    
    def timerEventGameFPS(self):
        self.pacmanList[0].process()
        for ghost in self.ghostList:
            ghost.process()
    
    def timerEventGhost(self):
        gl = self.ghostList
        if not gl[1].free:
            gl[1].free = True
        elif not gl[3].free:
            gl[3].free = True
        else:
            self.timerGhost.stop()
    
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
        self.settings.ghostIntersectionList = self.ghostIntersectionList
        self.createBodies()
        print("GameW set")
    
    def setupPhysicsForBodies(self):
        pass
    
    def paintEvent(self, e):
        painter = QPainter()
        painter.begin(self)
        
        painter.drawPixmap(0,0,self.settings.gameAreaSize[0],
                           self.settings.gameAreaSize[1], self.backgroundImage)
        
        self.drawBodyList(self.fruitList, painter)
        self.drawBodyList(self.powerupList, painter)
        self.drawBodyList(self.ballList, painter)
        self.drawBodyList(self.ghostList, painter)
        self.drawBodyList(self.pacmanList, painter)
        """
        self.drawGhostIntersections(painter) # Debug
        self.drawMowementMatrix(painter) # Debug
        """
        painter.end()
    
    def drawGhostIntersections(self, painter):
        # For debug purposes.
        painter.setPen(QPen())
        painter.setBrush(Qt.red)
        k = self.settings.corScale
        (xOffset, yOffset) = self.settings.corOffset
        size = k/2
        for cor in self.ghostIntersectionList:
            painter.drawRect(k*(cor[0] + xOffset) -size/2, k*(cor[1] + yOffset) -size/2, size, size)
    
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
                    painter.drawRect(k*(i + xOffset) -size/2, k*(j + yOffset) -size/2, size, size)
    
    def drawBodyList(self, bodyList, painter):
        for b in bodyList:
            b.draw(painter)
    
    def generateCoordinates(self):
        self.pacmanCor = [(13.5,23)]
        self.fruitCor = [(13.5,17)]
        self.ghostCors = [(13.5,11),(12,14),(14,14),(16,14)]
        self.ballCors = self.generateBallGCoordinateList()
        self.powerupCors = [(1,3), (26,3), (1,23), (26,23)]
        self.movementMatrix = self.generateMovementMatrix()
        self.ghostIntersectionList = self.generateGhostIntersectionList()
    
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
        
        corsAccessibleToGhosts = [(14,12),(13,14),(15,14)]
        for i in [12,14,16]:
            for j in range(13,16):
                corsAccessibleToGhosts.append((i,j))
        self.placeValueInMatrixOnListCoordinates(2, m, corsAccessibleToGhosts)
        
        return(m)
    
    @staticmethod
    def placeValueInMatrixOnListCoordinates(value, matrix, corList):
        for corTupple in corList:
            matrix[corTupple[0]][corTupple[1]] = value
    
    @staticmethod
    def generateGhostIntersectionList():
        return([(6,1),(21,1),
                (1,5),(6,5),(9,5),(12,5),(15,5),(18,5),(21,5),(26,5),
                (6,8),(21,8),
                (12,11),(15,11),
                (6,14),(9,14),(18,14),(21,14),
                    (12,14),(14,14),(16,14),
                (9,17),(18,17),
                (6,20),(9,20),(18,20),(21,20),
                (6,23),(9,23),(12,23),(15,23),(18,23),(21,23),
                (3,26),(24,26),
                (12,29),(15,29)])
    
    def modifyCoordinateLists(self):
        self.pacmanCor         = self.modifyTuppleList(self.pacmanCor)
        self.fruitCor          = self.modifyTuppleList(self.fruitCor)
        self.ghostCors         = self.modifyTuppleList(self.ghostCors)
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
        self.fruitList      = self.createBodyListFromCorList("Fruit", self.fruitCor)
        self.ghostList      = self.createBodyListFromCorList("Ghost", self.ghostCors)
        i = 0
        for ghost in self.ghostList:
            ghost.setGhostIndex(i)
            i += 1
        self.ballList       = self.createBodyListFromCorList("Ball", self.ballCors)
        self.powerupList    = self.createBodyListFromCorList("Powerup", self.powerupCors)
        # pacman created last, so it can setup it's collisionDetection
        self.pacmanList     = self.createBodyListFromCorList("Pacman", self.pacmanCor)
    
    def createBodyListFromCorList(self, BodyClass, CorList):
        list = []
        for cor in CorList:
            bodyInput = [cor, self.settings]
            if BodyClass == "Pacman":
                bodyInput = [cor, self.settings, self.keyHandler, self]
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
