"""
    Handles characters, meaning packman and the ghosts.
    
    Ghost AI:
        http://gameinternals.com/post/2072558330/understanding-pac-man-ghost-behavior
"""

#from sound import PlaySound

from physics import Movement, GhostAI, PacmanCollisionDetection

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
    
    def setGCor(self, corScale, corOffset):
        self.x0 = ((self.x + self.size/2)/corScale - corOffset[0])
        self.y0 = ((self.y + self.size/2)/corScale - corOffset[1])

    def setSize(self, settings):
        self.size = 1
    
    def moveToStart(self):
        self.x = self.xStart
        self.y = self.yStart
        self.alive = True
        self.setParameters()
    
    def setParameters(self):
        pass
    
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

class Pacman(Body, Movement, PacmanCollisionDetection):
    def __init__(self, bodyInput):
        [coordinateTupple, settings, keyHandler, GameW] = bodyInput
        self.corScale = settings.corScale
        self.corOffset = settings.corOffset
        Body.__init__(self, [coordinateTupple, settings])
        Movement.__init__(self, settings, [1])
        PacmanCollisionDetection.__init__(self, GameW.ghostList, GameW.ballList, GameW.powerupList, GameW.fruitList)
        self.keyHandler = keyHandler
        self.colour = settings.PACMANCOLOUR
        self.speed = settings.PACMANSPEED
        self.mouthAngleSpeed = settings.PACMANMOUTHANGLESPEED
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
        self.extraLives = 3
        self.moving = False
    
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
        if self.alive:
            pKey = self.keyHandler.pressedKey
            if pKey:
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
            self.checkCollisions()
    
    def move(self):
        self.pMove()
        self.setHitbox()
        if self.moving:
            self.moveMouth()
    
    def moveMouth(self):
        self.pMoveMouth()
        self.firstAngle = 90*self.direction + self.halfAngleOfMouth
        self.spanAngle = 360 - 2*self.halfAngleOfMouth
    
    def gotEaten(self):
        self.alive = False
        self.extraLives -= 1
        print("U DED!\tExtra lives left:", self.extraLives)
    
    def ateGhost(self):
        # you get points and maby extra lives?
        pass
    
    def ateBall(self):
        # points
        pass
    
    def atePowerup(self):
        print("SO STRONK!")
    
    def ateFruit(self):
        print("MUCH POINTS!")

class Ghost(Body, Movement, GhostAI):
    def __init__(self, bodyInput):
        [coordinateTupple, settings] = bodyInput
        self.corScale = settings.corScale
        self.corOffset = settings.corOffset
        Body.__init__(self, bodyInput)
        Movement.__init__(self, settings, [1,2])
        GhostAI.__init__(self, settings)
        self.ghostColourList = settings.GHOSTCOLOURLIST
        self.colour = Qt.green
        self.fastSpeed = settings.GHOSTSPEED
        self.slowSpeed = settings.SLOWGHOSTSPEED
        self.speed = self.fastSpeed
        self.setMovement()
    
    def setSize(self, settings):
        self.size = settings.GHOSTSIZE
    
    def setParameters(self):
        self.chasing = True
    
    def setGhostIndex(self, ghostIndex):
        self.ghostIndex = ghostIndex # is integer 0,1,2 or 3
        try:
            self.colour = self.ghostColourList[self.ghostIndex]
        except IndexError:
            self.colour = Qt.green
        self.setBeginningDirection()
    
    def setBeginningDirection(self):
        if self.ghostIndex == 0:
            self.direction = LEFT
            self.free = True
        elif self.ghostIndex == 1:
            self.direction = UP
            self.free = False
        elif self.ghostIndex == 2:
            self.direction = DOWN
            self.free = True
        elif self.ghostIndex == 3:
            self.direction = DOWN
            self.free = False
    
    def draw(self, painter):
        Body.draw(self, painter)
        painter.setBrush(self.colour)
        painter.drawRect(self.x, self.y, self.size, self.size)
    
    def process(self):
        self.AIProcess()
    
    def gotEaten(self):
        self.alive = False

class Ball(Body):
    def __init__(self, bodyInput):
        super().__init__(bodyInput)
        [coordinateTupple, settings] = bodyInput
        self.colour = settings.BALLCOLOUR
        self.setGCor(settings.corScale, settings.corOffset)
    
    def setSize(self, settings):
        self.size = settings.BALLSIZE
    
    def hide(self):
        self.x = -10
        self.y = -10
        self.alive = False
    
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