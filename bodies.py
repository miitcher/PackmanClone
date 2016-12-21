"""
    Handles characters, meaning packman and the ghosts.
"""

#from sound import PlaySound

from physics import Movement

from PySide.QtCore import *
from PySide.QtGui import *

# Directions
LEFT  = 0
RIGHT = 1
UP    = 2
DOWN  = 3
OPENING = 4
CLOSING = 5


class MovementNodes():
    """
    Pacman and the ghosts can move on the 
    lines between the movement points.
    Therefore the walls don't need hitboxes.
    """
    def __init__(self):
        self.list = [(1,1),(6,1),(12,1),(15,1),(21,1),(26,1),
                     (1,5),(6,5),(9,5),(12,5),(15,5),(18,5),(21,5),(26,5),
                     (1,8),(6,8),(9,8),(12,8),(15,8),(18,8),(21,8),(26,8),
                     (9,11),(12,11),(13,11),(14,11),(15,11),(18,11),
                     (-1,14),(6,14),(9,14),(11,14),(13,14),(14,14),
                        (16,14),(18,14),(21,14),(28,14),
                     (9,17),(18,17),
                     (1,20),(6,20),(9,20),(12,20),(15,20),(18,20),(21,20),(26,20),
                     (1,23),(3,23),(6,23),(9,23),(12,23),(15,23),(18,23),(21,23),(24,23),(26,23),
                     (1,26),(3,26),(6,26),(9,26),(12,26),(15,26),(18,26),(21,26),(24,26),(26,26),
                     (1,29),(12,29),(15,29),(26,29)]

class Body(Movement):
    def __init__(self, bodyInput):
        [coordinateTupple, settings] = bodyInput
        super().__init__(settings.getFPS())
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
    
    def move(self):
        [self.x, self.y] = self.pMove(self.x, self.y, self.direction, self.speed)
        self.setHitbox()
    
    def draw(self, painter):
        painter.setBrush(QBrush())
        painter.setPen(QPen())

class Pacman(Body):
    def __init__(self, bodyInput):
        [coordinateTupple, settings, keyHandler] = bodyInput
        super().__init__([coordinateTupple, settings])
        self.movementNodeCors = settings.movementNodeCors
        self.keyHandler = keyHandler
        self.colour = settings.PACMANCOLOUR
        self.speed = settings.PACMANSPEED
        self.mouthAngleSpeed = settings.PACMANMOUTHANGLESPEED
        self.setParameters()
    
    def setSize(self, settings):
        self.size = settings.PACMANSIZE
        self.maxHalfAngleOfMouth = settings.PACMANMAXMOUTHANGLE / 2
    
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
    
    def setThings(self, settings):
        # Map keys
        keySettingsDict = settings.keySettingsDict
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
        [self.halfAngleOfMouth, self.mouthMovementDirection] = self.pMoveMouth(
                                                                    self.halfAngleOfMouth,
                                                                    self.mouthMovementDirection,
                                                                    self.mouthAngleSpeed,
                                                                    self.maxHalfAngleOfMouth)
        self.firstAngle = self.baseAngle + self.halfAngleOfMouth
        self.spanAngle = 360 - 2*self.halfAngleOfMouth

class Ghost(Body):
    def __init__(self, bodyInput):
        super().__init__(bodyInput)
        [coordinateTupple, settings] = bodyInput
        self.movementNodeCors = settings.movementNodeCors
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

class Wall(Body):
    def __init__(self, bodyInput):
        super().__init__(bodyInput)
        [coordinateTupple, settings] = bodyInput
        self.wallThickness = settings.WALLTHICKNESS
        self.colour = settings.WALLCOLOUR
    
    def setSize(self, settings):
        self.size = settings.WALLLENGTH
    
    def setThings(self, settings):
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
    def __init__(self, bodyInput):
        super().__init__(bodyInput)
        #[coordinateTupple, settings] = bodyInput

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
        #self.colour = settings.FRUITCOLOUR
    
    def setSize(self, settings):
        self.size = settings.FRUITSIZE