"""
    Handles characters, meaning packman and the ghosts.
"""

#from sound import PlaySound

from PySide.QtCore import *
from PySide.QtGui import *

# Directions
LEFT  = 0
RIGHT = 1
UP    = 2
DOWN  = 3
# Relative sizes [GCor]
WALLTHICKNESS   = 0.1
PACMANSIZE      = 2 - 4*WALLTHICKNESS
GHOSTSIZE       = PACMANSIZE
BALLSIZE        = 0.3
POWERUPSIZE     = 0.8
FRUITSIZE       = POWERUPSIZE

WALLCOLOUR      = Qt.blue
PACMANCOLOUR    = Qt.yellow
GHOSTCOLOURLIST = [Qt.red, Qt.cyan, QColor(255,192,203), QColor(255,165,0)]
# red, cyan, pink, orange
BALLCOLOUR      = QColor(255,204,153)
POWERUPCOLOUR   = BALLCOLOUR
FRUITCOLOUR     = Qt.red
# Speeds [GCor/s]
PACMANSPEED     = 2
GHOSTSPEED      = PACMANSPEED
SLOWGHOSTSPEED  = GHOSTSPEED/2

def setupBodyList(BodyClass, quantity, MWindow):
    list = []
    for i in range(quantity):
        if BodyClass == "Ghost":
            list.append(Ghost(MWindow, i))
        elif BodyClass == "Wall":
            list.append(Wall(MWindow))
        elif BodyClass == "GhostWall":
            list.append(GhostWall(MWindow))
        elif BodyClass == "Ball":
            list.append(Ball(MWindow))
        elif BodyClass == "Powerup":
            list.append(Powerup(MWindow))
    return list

def setupGhostList(MWindow, quantity):
    return setupBodyList("Ghost", quantity, MWindow)

def setupWallList(MWindow, quantity):
    return setupBodyList("Wall", quantity, MWindow)

def setupGhostWallList(MWindow, quantity):
    return setupBodyList("GhostWall", quantity, MWindow)

def setupBallList(MWindow, quantity):
    return setupBodyList("Ball", quantity, MWindow)

def setupPowerupList(MWindow, quantity):
    return setupBodyList("Powerup", quantity, MWindow)


class Body():
    def __init__(self, MWindow):
        self.MWindow = MWindow
    
    def setStartCoordinateAndScale(self, coordinateTupple):
        xRaw = coordinateTupple[0]
        yRaw = coordinateTupple[1]
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
    
    def moveToStart(self):
        self.x = self.xStart
        self.y = self.yStart
    
    def physicsMove(self):
        return self.MWindow.physics.move(self.x, self.y, self.direction, self.speed)
    
    def setThings(self):
        pass
    
    def setHitbox(self):
        # The hitbox is a rectangle
        self.HBLeft  = self.x
        self.HBRight = self.x + self.size
        self.HBUp    = self.y
        self.HBDown  = self.y + self.size
    
    def draw(self, painter):
        painter.setBrush(QBrush())
        painter.setPen(QPen())

class Pacman(Body):
    def __init__(self, MWindow):
        super().__init__(MWindow)
        self.size = PACMANSIZE
        self.colour = PACMANCOLOUR
        self.direction = RIGHT
        self.speed = PACMANSPEED
        self.firstAngle = 50*16
        self.spanAngle = 260*16
        
        self.alive = True
        self.extraLives = 3
        self.moving = False
        self.nextDirection = None
    
    def setThings(self):
        # Map keys
        keySettingsDict = self.MWindow.settings.keySettingsDict
        self.MoveLeft = keySettingsDict["MoveLeft"]
        self.MoveRight = keySettingsDict["MoveRight"]
        self.MoveUp = keySettingsDict["MoveUp"]
        self.MoveDown = keySettingsDict["MoveDown"]
    
    def draw(self, painter):
        Body.draw(self, painter)
        painter.setBrush(self.colour)
        painter.drawPie(self.x, self.y, self.size, self.size, self.firstAngle, self.spanAngle)
    
    def processPressedKey(self):
        pKey = self.MWindow.keyHandler.pressedKey
        if self.alive and pKey:
            print(pKey,"pressed")
            if pKey in self.MoveLeft:
                self.moving = True
                self.direction = LEFT
            elif pKey in self.MoveRight:
                self.moving = True
                self.direction = RIGHT
            elif pKey in self.MoveUp:
                self.moving = True
                self.direction = UP
            elif pKey in self.MoveDown:
                self.moving = True
                self.direction = DOWN
            self.MWindow.keyHandler.pressedKey = None
        if self.moving:
            self.move()
    
    def move(self):
        [self.x, self.y] = self.physicsMove()
        self.setHitbox()

class Ghost(Body):
    def __init__(self, MWindow, ghostIndex):
        self.size = GHOSTSIZE
        super().__init__(MWindow)
        self.ghostIndex = ghostIndex
        self.colour = Qt.green
        self.speed = GHOSTSPEED
    
    def setThings(self):
        try:
            self.colour = GHOSTCOLOURLIST[self.ghostIndex]
        except IndexError:
            self.colour = Qt.green
    
    def changeDirection(self, direction):
        self.direction = direction
    
    def draw(self, painter):
        Body.draw(self, painter)
        painter.setBrush(self.colour)
        painter.drawRect(self.x, self.y, self.size, self.size)

class Wall(Body):
    def __init__(self, MWindow):
        super().__init__(MWindow)
        self.size = 1
        self.wallThickness = WALLTHICKNESS
        self.colour = WALLCOLOUR
    
    def setThings(self):
        # vertical line
        self.startPoint = QPoint(self.x + self.size/2, self.y)
        self.endPoint   = QPoint(self.x + self.size/2, self.y + self.size)
        # horisontal line
        self.startPoint2 = QPoint(self.x, self.y + self.size/2)
        self.endPoint2   = QPoint(self.x + self.size, self.y + self.size/2)
    
    def draw(self, painter):
        Body.draw(self, painter)
        pen = QPen(self.colour, self.wallThickness, Qt.SolidLine)
        painter.setPen(pen)
        painter.drawLine(self.startPoint, self.endPoint)
        painter.drawLine(self.startPoint2, self.endPoint2)

class GhostWall(Wall):
    def __init__(self, MWindow):
        super().__init__(MWindow)

class Ball(Body):
    def __init__(self, MWindow):
        super().__init__(MWindow)
        self.size = BALLSIZE
        self.colour = BALLCOLOUR
    
    def draw(self, painter):
        Body.draw(self, painter)
        painter.setBrush(self.colour)
        painter.drawEllipse(self.x, self.y, self.size, self.size)

class Powerup(Ball):
    def __init__(self, MWindow):
        super().__init__(MWindow)
        self.size = POWERUPSIZE
        self.colour = POWERUPCOLOUR

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
        self.size = FRUITSIZE
        self.colour = FRUITCOLOUR