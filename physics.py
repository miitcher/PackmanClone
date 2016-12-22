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
    def __init__(self, fps):
        self.dt = 1 / fps # smallest time in physics
    
    def pMove(self, x, y, direction, speed, movementMatrix):
        change = self.dt * speed
        if direction == LEFT:
            return(x - change, y)
        elif direction == RIGHT:
            return(x + change, y)
        elif direction == UP:
            return(x, y - change)
        elif direction == DOWN:
            return(x, y + change)
    
    def pMoveMouth(self, angle, direction, angleSpeed, maxAngle):
        if direction == OPENING:
            newAngle = angle + self.dt * angleSpeed
            if maxAngle < newAngle:
                newAngle = angle
                direction = CLOSING
        elif direction == CLOSING:
            newAngle = angle - self.dt * angleSpeed
            if newAngle < 0:
                newAngle = angle
                direction = OPENING
        return(newAngle, direction)

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