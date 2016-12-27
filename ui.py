"""
    Handles users inputs and settings.
    
    Maby usefull:
        http://stackoverflow.com/questions/19122345/to-convert-string-to-variable-name
"""

from PySide.QtCore import Qt
from PySide.QtGui import QWidget, QColor


class SettingsError(Exception):
    pass

class KeyHandler():
    def __init__(self):
        self.pressedKey = None # format in strings: "Key_G"
    
    def keyPressed(self, currentWidget, e):
        self.currentWidget = str(currentWidget)
        self.pressedKey = str(Qt.Key(e.key())).split(".")[-1]

class Settings():
    """
    Settings stored in dictionaries:
        self.keySettingsDict
        self.otherSettingsDict
    How to change settings:
        self.keySettingsDict[setting] = keySList
        self.otherSettingsDict[setting] = valueList
        --> After changing a dictionary; writeSettingsToFile().
    """
    def __init__(self):
        self.minorProblems = []
        try:
            self.getSettingsFromFile()
        except FileNotFoundError:
            self.setDefaultSettings()
        self.processSettingsChanged()
    
    def __str__(self):
        s = "\tSETTINGS\nKEYS"
        for i in self.keySettingsDict:
            s += "\n" + i + ":\t" + str(self.keySettingsDict[i])
        s += "\nOTHER"
        for i in self.otherSettingsDict:
            s += "\n" + i + ":\t" + str(self.otherSettingsDict[i])
        return s
    
    def getSettingsFromFile(self):
        self.keySettingsDict = {}
        self.otherSettingsDict = {}
        with open("settings.ini", "r") as f:
            line = f.readline()
            while line != "":
                line = line.strip()
                if line[0] != "#":
                    isHeader = False
                    if line == "KEYS":
                        mode = "key"
                        isHeader = True
                    elif line == "OTHER":
                        mode = "other"
                        isHeader = True
                    if not isHeader:
                        try:
                            [setting, vstr] = line.split("=")
                            setting = setting.strip()
                            valsPre = vstr.split(",")
                            vals = []
                            if mode == "key":
                                for k in valsPre:
                                    keyStr = "Key_" + k.strip()
                                    vals.append(keyStr)
                                self.keySettingsDict[setting] = vals
                            elif mode == "other":
                                for v in valsPre:
                                    valStr = v.strip()
                                    vals.append(valStr)
                                self.otherSettingsDict[setting] = vals
                        except ValueError:
                            raise SettingsError('Line in "setting.ini" could not be read. Delete "settings.ini"-file.')
                line = f.readline()
    
    def writeSettingsToFile(self):
        with open("settings.ini", "w") as f:
            f.write("# SETTINGS\nKEYS")
            self.writeSettingsFromOneDict(f, self.keySettingsDict)
            f.write("\nOTHER")
            self.writeSettingsFromOneDict(f, self.otherSettingsDict)
    
    @staticmethod
    def writeSettingsFromOneDict(file, dict):
        for i in dict:
            line = "\n" + i + " = "
            c = 1
            for v in dict[i]:
                if c > 1:
                    line += ", "
                line += v.replace("Key_","")
                c += 1
            file.write(line)
    
    def setDefaultSettings(self):
        # creates the "settings.ini"-file, or overwrites it if it exists
        self.keySettingsDict = {
        "MoveUp" : ["Key_Up", "Key_W"],
        "MoveDown" : ["Key_Down", "Key_S"],
        "MoveRight" : ["Key_Right", "Key_D"],
        "MoveLeft" : ["Key_Left", "Key_A"],
        "Pause" : ["Key_Space"],
        "Esc" : ["Key_Escape"]}
        self.otherSettingsDict = {
        "Resolution" : ["1280x720"],
        "FPS" : ["60"],
        "WindowMode" : ["Windowed"], # Windowed / Fullscreen
        "MenuScale" : ["0.75"]} # Size of menu compared to resolution
        self.writeSettingsToFile()
    
    def checkIfKeysUsedByOtherSetting(self, choosenSetting, keySListRef):
        # returns dictionary of lists of used keys, with setting as index in dictionary
        usedKeysDict = {}
        for i in self.keySettingsDict:
            if i == choosenSetting:
                continue
            keySList = self.keySettingsDict[i]
            usedKeySList = []
            for k in keySList:
                if k in keySListRef:
                    usedKeySList.append(k)
            if usedKeySList:
                usedKeysDict[i] = usedKeySList
        if not usedKeysDict:
            return(None)
        else:
            return(usedKeysDict)
    
    def unassignKeysForSettings(self, removeKeySDict):
        # used with resulting dictionary from method checkIfKeysUsedByOtherSetting
        for i in removeKeySDict:
            removeKeySList = removeKeySDict[i]
            keySList = self.keySettingsDict[i]
            for k in removeKeySList:
                keySList.remove(k)
            self.keySettingsDict[i] = keySList
    
    def findKeyMeaning(self, key):
        keyS = str(key).split(".")[-1]
        for i in self.keySettingsDict:
            for k in self.keySettingsDict[i]:
                if k == keyS:
                    return(i)
        return None
    
    def processSettingsChanged(self):
        #Called when settings changed.
        self.makeOtherSettingsAccessible()
        self.calculateCorScaleAndCorOffset()
        self.setVariables()
    
    def makeOtherSettingsAccessible(self):
        """
        Needs to be called if you want to access
        the updated otherSettings.
        """
        settingsNotReadList = []
        # Resolution
        try:
            [w,h] = self.otherSettingsDict["Resolution"][0].split("x")
            self.width = int(w)
            self.height = int(h)
        except Exception:
            settingsNotReadList.append("Resolution")
            self.width = 1280
            self.height = 720
        # FPS & GFPS (Graphical frames per second)
        try:
            rawFps = int(self.otherSettingsDict["FPS"][0])
            if rawFps < 20:
                self.fps = 60
            else:
                self.fps = rawFps
            self.gfps = 20 * ( 1 + round(self.fps/20) )
        except Exception:
            settingsNotReadList.append("FPS")
            self.fps = 60
            self.gfps = self.fps + 20
        # MenuScale
        try:
            self.menuScale = float(self.otherSettingsDict["MenuScale"][0])
        except Exception:
            settingsNotReadList.append("MenuScale")
            self.menuScale = 0.75
        # WindowMode
        try:
            self.windowMode = self.otherSettingsDict["WindowMode"][0].strip()
        except Exception:
            settingsNotReadList.append("WindowMode")
            self.windowMode = "Windowed"
        
        if settingsNotReadList:
            s = "Settings "
            c = len(settingsNotReadList)
            for i in settingsNotReadList:
                s += i
                c -= 1
                if c > 0:
                    s += ", "
            s += ' could not be read, so default settings are used.\tFix problem by deleting "settings.ini"-file.'
            self.minorProblems.append(s)
    
    def calculateCorScaleAndCorOffset(self):
        """
        "corScale" is the ratio between the pixel- and 
        general coordinates (corScale = PixelCor / GeneralCor).
        
        The GeneralCor game-areas coordinate ranges are:
            x: [0, 27], y: [0, 30]
        We give extra space, in GeneralCor units:
            right/left: 1, up: 3, down: 2
        Extra spaces combined is:
            horisontal: 2, vertical: 5
        Now our GeneralCor side lenghts are:
            x: 29, y: 35
        The extra space up and left need buffers.
        """
        self.corOffset = (1,3)
        xLenGCor = 29   # 27 + 2
        yLenGCor = 35   # 30 + 5
        xRatio = self.width  / xLenGCor
        yRatio = self.height / yLenGCor
        # We determine the conversion between GCor
        # and PCor with the limiting length.
        if xRatio > yRatio:
            # height (y) limits
            self.corScale = yRatio
        else:
            # width (x) limits
            self.corScale = xRatio
        
        self.gameAreaSize = (self.corScale * xLenGCor,
                             self.corScale * yLenGCor)
    
    def setVariables(self):
        """
        Needs to be called if you want to access
        the variables.
        """
        k = self.corScale
        print(k)
        # Relative sizes [k * GCor]
        self.WALLTHICKNESS   = k * 0.1
        self.WALLLENGTH      = k * 1
        self.PACMANSIZE      = k * 2 - (4 * self.WALLTHICKNESS)
        self.GHOSTSIZE       = self.PACMANSIZE
        self.BALLSIZE        = k * 0.3
        self.POWERUPSIZE     = self.BALLSIZE * 2.6
        self.FRUITSIZE       = self.POWERUPSIZE
        # Angle [degrees]
        self.PACMANMAXMOUTHANGLE = 100
        # Angle speed [degrees/s]
        self.PACMANMOUTHANGLESPEED    = self.PACMANMAXMOUTHANGLE * 10
        # Speeds [k * GCor/s]
        self.PACMANSPEED     = k * 10
        self.GHOSTSPEED      = self.PACMANSPEED
        self.SLOWGHOSTSPEED  = self.GHOSTSPEED/2
        # Colours
        self.WALLCOLOUR      = Qt.blue
        self.PACMANCOLOUR    = Qt.yellow
        self.GHOSTCOLOURLIST = [Qt.red, Qt.cyan, QColor(255,192,203), QColor(255,165,0)]
                                # red, cyan, pink, orange
        self.BALLCOLOUR      = QColor(255,204,153)
        self.POWERUPCOLOUR   = self.BALLCOLOUR
        self.FRUITCOLOUR     = Qt.red