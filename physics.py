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


class Physics():
    def __init__(self):
        pass
    
    def setupPhysics(self, fps):
        self.dt = 1 / fps # smallest time in physics
    
    def move(self, x, y, direction, speed):
        change = self.dt * speed
        if direction == LEFT:
            return(x - change, y)
        elif direction == RIGHT:
            return(x + change, y)
        elif direction == UP:
            return(x, y - change)
        elif direction == DOWN:
            return(x, y + change)
    
    def moveMouth(self, angle, direction, angleSpeed, maxAngle):
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