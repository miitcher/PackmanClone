"""
    Handles character.
"""

from sound import PlaySound

class Character():
    def __init__(self, MWindow):
        self.MWindow = MWindow
        self.moveToStart()
    
    def moveToStart(self):
        self.x = 0
        self.y = 0
    
    def eat(self, food):
        # character closes and opens mouth and sound is played
        if food == "ball":
            PlaySound("eatBall")
        elif food == "powerupBall":
            PlaySound("eatPowerupBall")
        elif food == "fruit":
            PlaySound("eatFruit")