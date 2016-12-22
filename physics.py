"""
    Handles collision between walls, ghosts and the character.
"""

# Directions
LEFT  = 0
RIGHT = 1
UP    = 2
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
        """
        Variables above could be moved into where they are used so
        for example when dir is left, you don't need to calculate xD.
        Do this later, when the whole method works properly.
        
        The threshold 0.001 could be determined assording to the
        resolution if needed. Check if it is needed.
        self.dLen should propably also depend on the resolution.
            If dLen is a weird size, mayby pacman can get stuck.
            Instead of choosing the dLen, you could move pacman/ghost
            when needed so it don't get stuck.
        
        Separate the current direction and the direction the key indicates.
        """
        
        if self.direction == LEFT:
            if yD < 0.001:
                if xD > 0.001 or self.movementMatrix[round(x0)-1][round(y0)] in self.accessibleNodesList:
                    self.x -= self.dLen
                else:
                    self.moving = False
            else:
                self.moving = False
        elif self.direction == RIGHT:
            if yD < 0.001:
                if xD > 0.001 or self.movementMatrix[round(x0)+1][round(y0)] in self.accessibleNodesList:
                    self.x += self.dLen
        elif self.direction == UP:
            if xD < 0.001:
                if yD > 0.001 or self.movementMatrix[round(x0)][round(y0)-1] in self.accessibleNodesList:
                    self.y -= self.dLen
        elif self.direction == DOWN:
            if xD < 0.001:
                if yD > 0.001 or self.movementMatrix[round(x0)][round(y0)+1] in self.accessibleNodesList:
                    self.y += self.dLen
        
        if self.moving:
            print("\nPacman GCor: ",x0,y0)
            print("xD & yD: ",xD,yD)
    
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