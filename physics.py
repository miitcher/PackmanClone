"""
    Handles collision between walls, ghosts and the character.
"""

class Physics():
    def __init__(self):
        pass
    
    def setRefresh(self, fps):
        self.dt = 1 / fps # smallest time in physics
    
    def move(self, x, y, direction, speed):
        pass