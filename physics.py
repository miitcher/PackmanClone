"""
    Handles collision between walls, ghosts and the character.
"""

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
        self.dt = 1 / settings.fps # smallest time
        self.corScale = settings.corScale
        self.corOffset = settings.corOffset
        self.movementMatrix = settings.movementMatrix
        self.accessibleNodesList = accessibleNodesList
    
    def setMovement(self):
        self.dLen = self.dt * self.speed # smallest length
        self.dAng = self.dt * self.mouthAngleSpeed # smallest angle
    
    def pMove(self):
        x0 = ((self.x + self.size/2)/self.corScale - self.corOffset[0])
        y0 = ((self.y + self.size/2)/self.corScale - self.corOffset[1])
        xD = abs(x0-round(x0))
        yD = abs(y0-round(y0))
        
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