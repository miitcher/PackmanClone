"""
    Handles collision between walls, ghosts and the character.
"""

from random import randint, choice

# Directions
LEFT  = 2
RIGHT = 0
UP    = 1
DOWN  = 3
OPENING = 4
CLOSING = 5


class Movement():
    """
    Evaluating movement.
    
    self.dLen = self.dt * self.speed
    self.dt = 1 / settings.fps
    self.PACMANSPEED = self.corScale * gCorSpeed
    Default: gCorSpeed = 10
             fps = 60
    
    dLen0   = dLen / corScale
            = dt * speed / corScale
            = (1/fps) * speed / corScale
            = (1/fps) * (corScale * gCorSpeed) / corScale
            = (1/fps) * gCorSpeed
            = gCorSpeed/fps
    The dLen0 only depends on the gCorSpeed and the fps.
    Pacman and ghosts start at gCoordinates of whole or half numbers.
    Therefore dLen0 must be 0.5/k, where k=[1,2,3,4,...]
    so the moving pacman or ghosts don't go outside the
    movementMatrix coordinates.
    We determine the fps:
    dLen0 = gCorSpeed/fps = 0.5/k , k=[1,2,3,4,...]
    --> fps = 2 * k * gCorSpeed
    If gCorSpeed = 10:
        fps = 20 * k , k=[1,2,3,4,...]
    We add the check of the fps, and correct it to the lower
    accepted fps-value.
    
    The threshold 0.001 is acceptable when we have choosen
    the suitable fps. It's used against rounding errors.
    """
    def __init__(self, settings, accessibleNodesList):
        self.dt = 1 / settings.gfps # smallest time
        self.corScale = settings.corScale
        self.corOffset = settings.corOffset
        self.movementMatrix = settings.movementMatrix
        self.accessibleNodesList = accessibleNodesList
    
    def setMovement(self):
        self.dLen = self.dt * self.speed # smallest length
        try:
            self.dAng = self.dt * self.mouthAngleSpeed # smallest angle
        except AttributeError:
            # the mouth angle is unique for pacman
            pass
    
    def pMove(self):
        x0 = ((self.x + self.size/2)/self.corScale - self.corOffset[0])
        y0 = ((self.y + self.size/2)/self.corScale - self.corOffset[1])
        xD = abs(x0-round(x0))
        yD = abs(y0-round(y0))
        
        # move trough "teleport"
        if round(y0) == 14:
            rx0 = round(x0)
            if rx0 == 0 and self.direction == LEFT and xD < 0.001:
                self.x = self.corScale * (self.corOffset[0] + 27) - self.size/2
                return
            if rx0 == 27 and self.direction == RIGHT and xD < 0.001:
                self.x = self.corScale * (self.corOffset[0]) - self.size/2
                return
        
        if self.direction == LEFT:
            if yD < 0.001 and (xD > 0.001 or self.movementMatrix[round(x0)-1][round(y0)] in self.accessibleNodesList):
                self.x -= self.dLen
            else:
                self.moving = False
        elif self.direction == RIGHT:
            if yD < 0.001 and (xD > 0.001 or self.movementMatrix[round(x0)+1][round(y0)] in self.accessibleNodesList):
                self.x += self.dLen
            else:
                self.moving = False
        elif self.direction == UP:
            if xD < 0.001 and (yD > 0.001 or self.movementMatrix[round(x0)][round(y0)-1] in self.accessibleNodesList):
                self.y -= self.dLen
            else:
                self.moving = False
        elif self.direction == DOWN:
            if xD < 0.001 and (yD > 0.001 or self.movementMatrix[round(x0)][round(y0)+1] in self.accessibleNodesList):
                self.y += self.dLen
            else:
                self.moving = False
    
    def pChangeDirection(self, newDirection):
        if self.atBeginning:
            typeStr = str(type(self))
            if typeStr == "<class 'bodies.Pacman'>":
                if newDirection in [UP, DOWN]:
                    return
                else:
                    self.atBeginning = False
        self.moving = True
        x0 = ((self.x + self.size/2)/self.corScale - self.corOffset[0])
        y0 = ((self.y + self.size/2)/self.corScale - self.corOffset[1])
        xD = abs(x0-round(x0))
        yD = abs(y0-round(y0))
        if newDirection == LEFT:
            if yD < 0.001 and (xD > 0.001 or self.movementMatrix[round(x0)-1][round(y0)] in self.accessibleNodesList):
                self.direction = newDirection
                self.nextDirection = None
            else:
                self.nextDirection = newDirection
        elif newDirection == RIGHT:
            if yD < 0.001 and (xD > 0.001 or self.movementMatrix[round(x0)+1][round(y0)] in self.accessibleNodesList):
                self.direction = newDirection
                self.nextDirection = None
            else:
                self.nextDirection = newDirection
        elif newDirection == UP:
            if xD < 0.001 and (yD > 0.001 or self.movementMatrix[round(x0)][round(y0)-1] in self.accessibleNodesList):
                self.direction = newDirection
                self.nextDirection = None
            else:
                self.nextDirection = newDirection
        elif newDirection == DOWN:
            if xD < 0.001 and (yD > 0.001 or self.movementMatrix[round(x0)][round(y0)+1] in self.accessibleNodesList):
                self.direction = newDirection
                self.nextDirection = None
            else:
                self.nextDirection = newDirection
    
    def pMoveMouth(self):
        if self.mouthMovementDirection == OPENING:
            newAngle = self.halfAngleOfMouth + self.dAng
            if self.maxHalfAngleOfMouth < newAngle:
                self.mouthMovementDirection = CLOSING
                return
        elif self.mouthMovementDirection == CLOSING:
            newAngle = self.halfAngleOfMouth - self.dAng
            if newAngle < 0:
                self.mouthMovementDirection = OPENING
                return
        self.halfAngleOfMouth = newAngle

class GhostAI():
    def __init__(self, settings):
        self.ghostIntersectionList = settings.ghostIntersectionList
        self.moving = True
    
    def AIProcess(self):
        if not self.free:
            return
        
        if self.moving:
            self.pMove()
            self.checkIntersection()
        else:
            self.newDirection()
    
    def newDirection(self):
        upDownList = [UP, DOWN]
        leftRightList = [LEFT, RIGHT]
        possibleDirections = self.possibleDirections()
        if self.direction in leftRightList:
            newDirection = choice(upDownList)
            while newDirection not in possibleDirections:
                newDirection = choice(upDownList)
        else:
            newDirection = choice(leftRightList)
            while newDirection not in possibleDirections:
                newDirection = choice(leftRightList)
        self.direction = newDirection
        self.moving = True
    
    def checkIntersection(self):
        x0 = ((self.x + self.size/2)/self.corScale - self.corOffset[0])
        y0 = ((self.y + self.size/2)/self.corScale - self.corOffset[1])
        xD = abs(x0-round(x0))
        yD = abs(y0-round(y0))
        
        if xD < 0.001 and yD < 0.001 and (round(x0),round(y0)) in self.ghostIntersectionList:
            if randint(0,1):
                self.newDirection()
    
    def possibleDirections(self):
        possibleDirections = []
        rx0 = round((self.x + self.size/2)/self.corScale - self.corOffset[0])
        ry0 = round((self.y + self.size/2)/self.corScale - self.corOffset[1])
        
        if self.movementMatrix[rx0-1][ry0] in self.accessibleNodesList:
            possibleDirections.append(LEFT)
        if self.movementMatrix[rx0+1][ry0] in self.accessibleNodesList:
            possibleDirections.append(RIGHT)
        if self.movementMatrix[rx0][ry0-1] in self.accessibleNodesList:
            possibleDirections.append(UP)
        if self.movementMatrix[rx0][ry0+1] in self.accessibleNodesList:
            possibleDirections.append(DOWN)
        return(possibleDirections)

class Collision():
    """
    A collision can happen between:
        pacman - ghost
        pacman - ball
        pacman - powerup
        pacman - fruit
    Walls don't have hitboxes because
    of the movwmentPoints.
    """
    def __init__(self):
        pass