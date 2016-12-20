"""
    Pacman Clone
    by Miitcher
    For fun project doing a Pacman clone.
    
    Python 3.4
    PySide #
"""

from graphics import MainWindow
from ui import Settings

import sys
from PySide.QtGui import QApplication


class Heart():
    def __init__(self):
        self.MWindow = MainWindow()
        self.settings = Settings()
        self.MWindow.setupWindow(self.settings)
        
        self.testing()
        
        self.MWindow.show()
    
    def testing(self):
        self.MWindow.toGameW()
        """
        g = self.MWindow.GameW
        print('\n', g.BODYLIST)
        print(g.ghostList)
        print(g.BODYLIST[0].x, g.BODYLIST[0].y)
        print(g.pacmanPCor, '\n')
        for i in g.ghostList:
            print(i.x, i.y)
        """
        #sys.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    heart = Heart()
    sys.exit(app.exec_())
