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
    Class used when moving pacman or ghosts.
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
        if self.previousDirection == None:
            if newDirection in [UP, DOWN]:
                return
        self.moving = True
        self.previousDirection = self.direction
        """
        self.direction = newDirection
        return
        """
        
        x0 = ((self.x + self.size/2)/self.corScale - self.corOffset[0])
        y0 = ((self.y + self.size/2)/self.corScale - self.corOffset[1])
        xD = abs(x0-round(x0))
        yD = abs(y0-round(y0))
        """
        The threshold 0.001 could be determined assording to the
        resolution if needed. Check if it is needed.
        
        self.dLen should propably also depend on the resolution.
            If dLen is a weird size, mayby pacman can get stuck.
            Instead of choosing the dLen, you could move pacman/ghost
            when needed so it don't get stuck.
        """
        """
        if self.moving:
            print("\nPacman GCor: ",x0,y0)
            print("xD & yD: ",xD,yD)
        """
        
        """
        Next thing: add the "buffer-turning" on other places than
        where pacman meets a wall.
        """
        
        if newDirection == LEFT:
            if yD < 0.001 and (xD > 0.001 or self.movementMatrix[round(x0)-1][round(y0)] in self.accessibleNodesList):
                self.direction = newDirection
            else:
                self.nextDirection = newDirection
        elif newDirection == RIGHT:
            if yD < 0.001 and (xD > 0.001 or self.movementMatrix[round(x0)+1][round(y0)] in self.accessibleNodesList):
                self.direction = newDirection
            else:
                self.nextDirection = newDirection
        elif newDirection == UP:
            if xD < 0.001 and (yD > 0.001 or self.movementMatrix[round(x0)][round(y0)-1] in self.accessibleNodesList):
                self.direction = newDirection
            else:
                self.nextDirection = newDirection
        elif newDirection == DOWN:
            if xD < 0.001 and (yD > 0.001 or self.movementMatrix[round(x0)][round(y0)+1] in self.accessibleNodesList):
                self.direction = newDirection
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