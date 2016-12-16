"""
    Handles graphics.
    https://wiki.qt.io/PySideDocumentation
"""

import sys
from PySide.QtCore import *
from PySide.QtGui import *


class MainWindow():
    pass


if __name__ == '__main__':
    print("lole")
    app = QApplication(sys.argv)
    
    w=QWidget()
    w.setWindowTitle("Nakeeko tata?")
    w.show()
    
    sys.exit(app.exec_())