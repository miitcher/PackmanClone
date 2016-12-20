"""
    Handles collision between walls, ghosts and the character.
"""

# Directions
LEFT  = 0
RIGHT = 1
UP    = 2
DOWN  = 3


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