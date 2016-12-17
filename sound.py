"""
    Handles sounds.
    
    Sounds to play:
        music (beginning and end)
        packman
            eating
                balls
                fruit
            dying
        ghost
            chasing
            beeing chased (blue)
            eaten
    
    Find what libraries can be used to play sounds.
        Depending what library is used for sound, will
        determine if there is many functions or just
        one class.
"""

from PySide.QtGui import QSound

soundDict = []
soundDict['musicBeginning'] = QSound('musicBeginning')

def playSound(soundName):
    soundDict[soundName].play()
    soundDict[soundName].stop()
