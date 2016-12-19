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
        self.xStart = coordinateTupple[0]
        self.yStart = coordinateTupple[1]
        self.PToG = PToG
        self.moveToStart()
        self.setScale()
        self.setHitbox()
    
    def setScale(self):
        # implemented in child
        # hitbox and other parameters set here
        self.r = 2*self.PToG
    
    def setHitbox(self):
        # The hitbox is a rectangle
        self.HBLeft  = self.x - self.r
        self.HBRight = self.x + self.r
        self.HBUp    = self.y - self.r
        self.HBDown  = self.y + self.r
    
    def moveToStart(self):
        self.x = self.xStart
        self.y = self.yStart
    
    def draw(self, painter):
        pass
    """
    def eat(self, food):
        # character closes and opens mouth and sound is played
        if food == "ball":
            PlaySound("eatBall")
        elif food == "powerupBall":
            PlaySound("eatPowerupBall")
        elif food == "fruit":
            PlaySound("eatFruit")
    """

class Pacman(Body):
    def __init__(self, MWindow):
        super().__init__(MWindow)
        self.direction = RIGHT
        self.firstAngle = 50*16
        self.spanAngle = 260*16
    
    def setScale(self):
        self.r = self.PToG * 0.95
    
    def changeDirectionTo(self, direction):
        self.direction = direction
    
    def draw(self, painter):
        painter.setBrush(Qt.yellow)
        print(self.x, self.y, self.r, self.r, self.firstAngle, self.spanAngle)
        painter.drawPie(self.x, self.y, self.r, self.r, self.firstAngle, self.spanAngle)

class Ghost(Body):
    def __init__(self, MWindow):
        super().__init__(MWindow)

class Wall(Body):
    def __init__(self, MWindow):
        super().__init__(MWindow)

class GhostWall(Wall):
    def __init__(self, MWindow):
        super().__init__(MWindow)

class Ball(Body):
    def __init__(self, MWindow):
        super().__init__(MWindow)
    
    def setScale(self):
        self.r = self.PToG * 0.3
    
    def draw(self, painter):
        painter.setBrush(Qt.yellow)
        """
        painter.setBrush(QBrush())
        pen = QPen(Qt.yellow, 1, Qt.SolidLine)
        painter.setPen(pen)
        """
        painter.drawEllipse(self.x, self.y, self.r, self.r)

class Powerup(Ball):
    def __init__(self, MWindow):
        super().__init__(MWindow)

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