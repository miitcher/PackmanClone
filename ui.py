"""
    Handles users inputs and settings.
    
    Maby usefull:
        http://stackoverflow.com/questions/19122345/to-convert-string-to-variable-name
"""

import PySide
from PySide.QtCore import Qt


def keyPressed(key, currentWidget):
    pass

class SettingsError(Exception):
    pass
    """def __init__(self, expression, message):
        self.expression = expression
        self.message = message"""

class Settings():
    def __init__(self):
        """
        Settings stored in dictionaries:
            self.keySettingsDict
            self.otherSettingsDict
        """
        try:
            self.getSettingsFromFile()
        except FileNotFoundError:
            self.setDefaultSettings()
    
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
            """
            for i in self.keySettingsDict:
                line = "\n" + i + " = "
                c = 1
                for k in self.keySettingsDict[i]:
                    if c > 1:
                        line += ", "
                    line += k.replace("Key_","")
                    c += 1
                f.write(line)
            """
            f.write("\nOTHER")
            self.writeSettingsFromOneDict(f, self.otherSettingsDict)
        print("Settings written to file")
    
    def writeSettingsFromOneDict(self, f, dict):
        for i in dict:
            line = "\n" + i + " = "
            c = 1
            for v in dict[i]:
                if c > 1:
                    line += ", "
                line += v.replace("Key_","")
                c += 1
            f.write(line)
    
    def findKeyMeaning(self, key):
        keyS = str(key).split(".")[-1]
        for i in self.keySettingsDict:
            for k in self.keySettingsDict[i]:
                if k == keyS:
                    return(i)
        return None
    
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
        "Resolution" : ["1280x720"]}
        self.writeSettingsToFile()
    
    def changeKeySetting(self, setting, keySList):
        self.keySettingsDict[setting] = keySList
    
    def changeOtherSetting(self, setting, valueList):
        self.otherSettingsDict[setting] = valueList
    
    def addKeyToKeySetting(self, setting, keyS):
        keySList = self.keySettingsDict[setting]
        keySList.append(keyS)
        self.keySettingsDict[setting] = keySList
    
    def unasignKeysForOtherSettings(self, choosenSetting, keySListUnasign):
        keysUnasigned = False
        for i in self.keySettingsDict:
            if i == choosenSetting:
                continue
            keySList = self.keySettingsDict[i]
            removeKeySList = []
            for k in keySList:
                if k in keySListUnasign:
                    removeKeySList.append(k)
                    keysUnasigned = True
            for k in removeKeySList:
                keySList.remove(k)
            self.keySettingsDict[i] = keySList
        return keysUnasigned


if __name__ == '__main__':
    settings = Settings()
    print(settings)
    settings.setDefaultSettings()
    print(settings)
    print("meaning for Qt.Key_S: ",settings.findKeyMeaning(Qt.Key_S))
    settings.changeKeySetting("MoveDown", ["Key_O", "Key_9"])
    settings.changeOtherSetting("Resolution", ["1920x1080"])
    settings.writeSettingsToFile()
    print(settings)
    settings.addKeyToKeySetting("MoveUp", "Key_Q")
    settings.writeSettingsToFile()
    print(settings)
    settings.unasignKeysForOtherSettings("MoveDown", ["Key_Up", "Key_9", "Key_Q", "Key_S"])
    settings.writeSettingsToFile()
    print(settings)
    