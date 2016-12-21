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
OPENING = 4
CLOSING = 5


class Body():
    def __init__(self, MWindow, coordinateTupple):
        self.settings = MWindow.settings
        self.physics = MWindow.physics
        self.keyHandler = MWindow.keyHandler
        xRaw = coordinateTupple[0]
        yRaw = coordinateTupple[1]
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
    
    def __str__(self):
        return("(%s, %s)" % (self.x, self.y))
    
    def setSize(self):
        self.size = 1
    
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
        self.HBList = [self.HBLeft, self.HBRight, self.HBUp, self.HBDown]
    
    def move(self):
        [self.x, self.y] = self.physics.move(self.x, self.y, self.direction, self.speed)
        self.setHitbox()
    
    def draw(self, painter):
        painter.setBrush(QBrush())
        painter.setPen(QPen())

class Pacman(Body):
    def __init__(self, MWindow, coordinateTupple):
        super().__init__(MWindow, coordinateTupple)
        self.colour = self.settings.PACMANCOLOUR
        self.speed = self.settings.PACMANSPEED
        self.mouthAngleSpeed = self.settings.PACMANMOUTHANGLESPEED
        self.setParameters()
    
    def setSize(self):
        self.size = self.settings.PACMANSIZE
        self.maxHalfAngleOfMouth = self.settings.PACMANMAXMOUTHANGLE / 2
    
    def setParameters(self):
        self.direction = RIGHT
        self.mouthMovementDirection = CLOSING
        self.halfAngleOfMouth = self.maxHalfAngleOfMouth
        self.firstAngle = self.maxHalfAngleOfMouth
        self.spanAngle = 360 - 2*self.maxHalfAngleOfMouth
        self.alive = True
        self.extraLives = 3
        self.moving = False
        self.nextDirection = None
    
    def moveToStart(self):
        Body.moveToStart(self)
        self.setParameters()
    
    def setThings(self):
        # Map keys
        keySettingsDict = self.settings.keySettingsDict
        self.MoveLeft = keySettingsDict["MoveLeft"]
        self.MoveRight = keySettingsDict["MoveRight"]
        self.MoveUp = keySettingsDict["MoveUp"]
        self.MoveDown = keySettingsDict["MoveDown"]
    
    def draw(self, painter):
        Body.draw(self, painter)
        painter.setBrush(self.colour)
        painter.drawPie(self.x, self.y, self.size, self.size, 16*self.firstAngle, 16*self.spanAngle)
    
    def processPressedKey(self):
        pKey = self.keyHandler.pressedKey
        if self.alive and pKey:
            #print(pKey,"pressed")
            if pKey in self.MoveLeft:
                self.moving = True
                self.direction = LEFT
                self.baseAngle = 180
            elif pKey in self.MoveRight:
                self.moving = True
                self.direction = RIGHT
                self.baseAngle = 0
            elif pKey in self.MoveUp:
                self.moving = True
                self.direction = UP
                self.baseAngle = 90
            elif pKey in self.MoveDown:
                self.moving = True
                self.direction = DOWN
                self.baseAngle = -90
            self.keyHandler.pressedKey = None
        if self.moving:
            self.move()
            self.moveMouth()
    
    def moveMouth(self):
        [self.halfAngleOfMouth, self.mouthMovementDirection] = self.physics.moveMouth(
                                                                    self.halfAngleOfMouth,
                                                                    self.mouthMovementDirection,
                                                                    self.mouthAngleSpeed,
                                                                    self.maxHalfAngleOfMouth)
        self.firstAngle = self.baseAngle + self.halfAngleOfMouth
        self.spanAngle = 360 - 2*self.halfAngleOfMouth

class Ghost(Body):
    def __init__(self, MWindow, coordinateTupple):
        super().__init__(MWindow, coordinateTupple)
        self.ghostColourList = self.settings.GHOSTCOLOURLIST
        self.colour = Qt.green
        self.speed = self.settings.GHOSTSPEED
        self.slowSpeed = self.settings.SLOWGHOSTSPEED
    
    def setSize(self):
        self.size = self.settings.GHOSTSIZE
    
    def setGhostIndex(self, ghostIndex):
        self.ghostIndex = ghostIndex
        try:
            self.colour = self.ghostColourList[self.ghostIndex]
        except IndexError:
            self.colour = Qt.green
    
    def draw(self, painter):
        Body.draw(self, painter)
        painter.setBrush(self.colour)
        painter.drawRect(self.x, self.y, self.size, self.size)

class Wall(Body):
    def __init__(self, MWindow, coordinateTupple):
        super().__init__(MWindow, coordinateTupple)
        self.wallThickness = self.settings.WALLTHICKNESS
        self.colour = self.settings.WALLCOLOUR
    
    def setSize(self):
        self.size = self.settings.WALLLENGTH
    
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
    def __init__(self, MWindow, coordinateTupple):
        super().__init__(MWindow, coordinateTupple)

class Ball(Body):
    def __init__(self, MWindow, coordinateTupple):
        super().__init__(MWindow, coordinateTupple)
        self.colour = self.settings.BALLCOLOUR
    
    def setSize(self):
        self.size = self.settings.BALLSIZE
    
    def draw(self, painter):
        Body.draw(self, painter)
        painter.setBrush(self.colour)
        painter.drawEllipse(self.x, self.y, self.size, self.size)

class Powerup(Ball):
    def __init__(self, MWindow, coordinateTupple):
        super().__init__(MWindow, coordinateTupple)
        self.colour = self.settings.POWERUPCOLOUR
    
    def setSize(self):
        self.size = self.settings.POWERUPSIZE
        

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
    def __init__(self, MWindow, coordinateTupple):
        super().__init__(MWindow, coordinateTupple)
        self.colour = self.settings.FRUITCOLOUR
    
    def setSize(self):
        self.size = self.settings.FRUITSIZE