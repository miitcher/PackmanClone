"""
    Handles characters, meaning packman and the ghosts.
"""

#from sound import PlaySound

from PySide.QtCore import *
from PySide.QtGui import *

LEFT  = 0
RIGHT = 1
UP    = 2
DOWN  = 3
# Relative sizes
PACKMANSIZE   = 0.95
GHOSTSIZE     = 0.95
BALLSIZE      = 0.25
POWERUPSIZE   = 0.7
FRUITSIZE     = 0.75
WALLTHICKNESS = 0.2


def setupBodyList(BodyClass, quantity, MWindow):
    list = []
    for i in range(quantity):
        if BodyClass == "Ghost":
            list.append(Ghost(MWindow))
        elif BodyClass == "Wall":
            list.append(Wall(MWindow))
        elif BodyClass == "GhostWall":
            list.append(GhostWall(MWindow))
        elif BodyClass == "Ball":
            list.append(Ball(MWindow))
        elif BodyClass == "Powerup":
            list.append(Powerup(MWindow))
    return list

def setupGhostList(MWindow):
    return setupBodyList("Ghost", 4, MWindow)

def setupWallList(MWindow):
    return setupBodyList("Wall", 458, MWindow)

def setupGhostWallList(MWindow):
    return setupBodyList("GhostWall", 22, MWindow)

def setupBallList(MWindow):
    return setupBodyList("Ball", 240, MWindow)

def setupPowerupList(MWindow):
    return setupBodyList("Powerup", 4, MWindow)


class Body():
    def __init__(self, MWindow):
        self.MWindow = MWindow
    
    def setStartCoordinateAndScale(self, coordinateTupple, PToG):
        xRaw = coordinateTupple[0]
        yRaw = coordinateTupple[1]
        self.PToG = PToG
        self.setSize()
        """
        When drawing a body, the coordinate will
        represent the upper-left-corner. Therefore
        the coordinate will need to corrected.
        """
        self.xStart = xRaw - self.size/2
        self.yStart = yRaw - self.size/2
        self.moveToStart()
        self.setThings()
        self.setHitbox()
    
    def setSize(self):
        self.size = self.PToG
    
    def moveToStart(self):
        self.x = self.xStart
        self.y = self.yStart
    
    def setThings(self):
        pass
    
    def setHitbox(self):
        # The hitbox is a rectangle
        self.HBLeft  = self.x
        self.HBRight = self.x + self.size
        self.HBUp    = self.y
        self.HBDown  = self.y + self.size
        # self.HBList  = [self.HBLeft, self.HBRight, self.HBUp, self.HBDown]
    
    def draw(self, painter):
        print("Not drawn: ",self)

class Pacman(Body):
    def __init__(self, MWindow):
        super().__init__(MWindow)
        self.direction = RIGHT
        self.firstAngle = 50*16
        self.spanAngle = 260*16
    
    def setSize(self):
        self.size = self.PToG * PACKMANSIZE
    
    def changeDirection(self, direction):
        self.direction = direction
    
    def draw(self, painter):
        painter.setBrush(Qt.yellow)
        painter.drawPie(self.x, self.y, self.size, self.size, self.firstAngle, self.spanAngle)

class Ghost(Body):
    def __init__(self, MWindow):
        super().__init__(MWindow)
    
    def setSize(self):
        self.size = self.PToG * GHOSTSIZE
    
    def changeDirection(self, direction):
        self.direction = direction
    
    def draw(self, painter):
        painter.setBrush(Qt.blue)
        painter.drawRect(self.x, self.y, self.size, self.size)

class Wall(Body):
    def __init__(self, MWindow):
        super().__init__(MWindow)
    
    def setThings(self):
        # ATM just vertical line
        self.startPoint = QPoint(self.x + self.size/2, self.y)
        self.endPoint   = QPoint(self.x + self.size/2, self.y + self.size)
        self.wallThickness = self.PToG * WALLTHICKNESS
    
    def draw(self, painter):
        pen = QPen(Qt.blue, self.wallThickness, Qt.SolidLine)
        painter.setPen(pen)
        painter.drawLine(self.startPoint, self.endPoint)

class GhostWall(Wall):
    def __init__(self, MWindow):
        super().__init__(MWindow)

class Ball(Body):
    def __init__(self, MWindow):
        super().__init__(MWindow)
        self.colour = Qt.yellow
    
    def setSize(self):
        self.size = self.PToG * BALLSIZE
    
    def draw(self, painter):
        painter.setBrush(self.colour)
        painter.drawEllipse(self.x, self.y, self.size, self.size)

class Powerup(Ball):
    def __init__(self, MWindow):
        super().__init__(MWindow)
        self.colour = Qt.magenta
    
    def setSize(self):
        self.size = self.PToG * POWERUPSIZE

class Fruit(Ball):
    """
    There is one fruit per level in the order:
        Cherry
        Strawberry
        Orange
        Apple
        Melon
        Galaxian
        Bell
        Key
    """
    def __init__(self, MWindow):
        super().__init__(MWindow)
        self.colour = Qt.red
    
    def setSize(self):
        self.size = self.PToG * FRUITSIZE