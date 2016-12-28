"""
    Handles characters, meaning packman and the ghosts.
"""

#from sound import PlaySound

from physics import Movement

from PySide.QtCore import *
from PySide.QtGui import *

# Directions
LEFT  = 2
RIGHT = 0
UP    = 1
DOWN  = 3
OPENING = 4
CLOSING = 5


class Body():
    def __init__(self, bodyInput):
        [coordinateTupple, settings] = bodyInput
        #super().__init__(settings.getFPS())
        xRaw = coordinateTupple[0]
        yRaw = coordinateTupple[1]
        self.setSize(settings)
        """
        When drawing a body, the coordinate will
        represent the upper-left-corner. Therefore
        the coordinate will need to corrected.
        """
        self.xStart = xRaw - self.size/2
        self.yStart = yRaw - self.size/2
        self.moveToStart()
        self.setThings(settings)
        self.setHitbox()
    
    def __str__(self):
        return("(%s, %s)" % (self.x, self.y))
    
    def setSize(self, settings):
        self.size = 1
    
    def moveToStart(self):
        self.x = self.xStart
        self.y = self.yStart
    
    def setThings(self, settings):
        pass
    
    def setHitbox(self):
        # The hitbox is a rectangle
        self.HBLeft  = self.x
        self.HBRight = self.x + self.size
        self.HBUp    = self.y
        self.HBDown  = self.y + self.size
        self.HBList = [self.HBLeft, self.HBRight, self.HBUp, self.HBDown]
    
    def draw(self, painter):
        painter.setBrush(QBrush())
        painter.setPen(QPen())

class Pacman(Body, Movement):
    def __init__(self, bodyInput):
        [coordinateTupple, settings, keyHandler] = bodyInput
        Body.__init__(self, [coordinateTupple, settings])
        Movement.__init__(self, settings, [1])
        self.keyHandler = keyHandler
        self.colour = settings.PACMANCOLOUR
        self.speed = settings.PACMANSPEED
        self.mouthAngleSpeed = settings.PACMANMOUTHANGLESPEED
        self.setParameters()
        self.setMovement()
    
    def setSize(self, settings):
        self.size = settings.PACMANSIZE
        self.maxHalfAngleOfMouth = settings.PACMANMAXMOUTHANGLE / 2
    
    def setParameters(self):
        self.atBeginning = True
        self.direction = RIGHT
        self.nextDirection = None
        self.mouthMovementDirection = CLOSING
        self.halfAngleOfMouth = self.maxHalfAngleOfMouth
        self.firstAngle = self.maxHalfAngleOfMouth
        self.spanAngle = 360 - 2*self.maxHalfAngleOfMouth
        self.baseAngle = 0
        self.alive = True
        self.extraLives = 3
        self.moving = False
    
    def moveToStart(self):
        Body.moveToStart(self)
        self.setParameters()
    
    def setThings(self, settings):
        # Map keys
        keySettingsDict = settings.keySettingsDict
        try:
            self.MoveLeft = keySettingsDict["MoveLeft"]
        except Exception:
            self.MoveLeft = ["Key_A"]
        try:
            self.MoveRight = keySettingsDict["MoveRight"]
        except Exception:
            self.MoveRight = ["Key_D"]
        try:
            self.MoveUp = keySettingsDict["MoveUp"]
        except Exception:
            self.MoveUp = ["Key_W"]
        try:
            self.MoveDown = keySettingsDict["MoveDown"]
        except Exception:
            self.MoveDown = ["Key_S"]
    
    def draw(self, painter):
        Body.draw(self, painter)
        painter.setBrush(self.colour)
        painter.drawPie(self.x, self.y, self.size, self.size, 16*self.firstAngle, 16*self.spanAngle)
    
    def process(self):
        pKey = self.keyHandler.pressedKey
        if self.alive and pKey:
            if pKey in self.MoveLeft:
                self.pChangeDirection(LEFT)
            elif pKey in self.MoveRight:
                self.pChangeDirection(RIGHT)
            elif pKey in self.MoveUp:
                self.pChangeDirection(UP)
            elif pKey in self.MoveDown:
                self.pChangeDirection(DOWN)
            self.keyHandler.pressedKey = None
        if self.moving:
            self.pChangeDirection(self.nextDirection)
            self.move()
    
    def move(self):
        self.pMove()
        self.setHitbox()
        if self.moving:
            self.moveMouth()
    
    def moveMouth(self):
        self.pMoveMouth()
        self.firstAngle = 90*self.direction + self.halfAngleOfMouth
        self.spanAngle = 360 - 2*self.halfAngleOfMouth

class Ghost(Body, Movement):
    def __init__(self, bodyInput):
        [coordinateTupple, settings] = bodyInput
        Body.__init__(self, bodyInput)
        Movement.__init__(self, settings, [1,2])
        self.ghostColourList = settings.GHOSTCOLOURLIST
        self.colour = Qt.green
        self.speed = settings.GHOSTSPEED
        self.slowSpeed = settings.SLOWGHOSTSPEED
    
    def setSize(self, settings):
        self.size = settings.GHOSTSIZE
    
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

class Ball(Body):
    def __init__(self, bodyInput):
        super().__init__(bodyInput)
        [coordinateTupple, settings] = bodyInput
        self.colour = settings.BALLCOLOUR
    
    def setSize(self, settings):
        self.size = settings.BALLSIZE
    
    def draw(self, painter):
        Body.draw(self, painter)
        painter.setBrush(self.colour)
        painter.drawEllipse(self.x, self.y, self.size, self.size)

class Powerup(Ball):
    def __init__(self, bodyInput):
        super().__init__(bodyInput)
        [coordinateTupple, settings] = bodyInput
        self.colour = settings.POWERUPCOLOUR
    
    def setSize(self, settings):
        self.size = settings.POWERUPSIZE
        

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
    def __init__(self, bodyInput):
        super().__init__(bodyInput)
        [coordinateTupple, settings] = bodyInput
        self.colour = settings.FRUITCOLOUR
    
    def setSize(self, settings):
        self.size = settings.FRUITSIZE