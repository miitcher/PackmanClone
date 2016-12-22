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
    def __init__(self, fps):
        self.dt = 1 / fps # smallest time in physics
    
    def pMove(self):
        """ movementMatrix
        """
        change = self.dt * self.speed
        if self.direction == LEFT:
            self.x -= change
        elif self.direction == RIGHT:
            self.x += change
        elif self.direction == UP:
            self.y -= change
        elif self.direction == DOWN:
            self.y += change
    
    def pMoveMouth(self):
        if self.mouthMovementDirection == OPENING:
            newAngle = self.halfAngleOfMouth + self.dt * self.mouthAngleSpeed
            if self.maxHalfAngleOfMouth < newAngle:
                self.mouthMovementDirection = CLOSING
                return
        elif self.mouthMovementDirection == CLOSING:
            newAngle = self.halfAngleOfMouth - self.dt * self.mouthAngleSpeed
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