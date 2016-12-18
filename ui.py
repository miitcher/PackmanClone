"""
    Handles users inputs and settings.
    
    Maby usefull:
        http://stackoverflow.com/questions/19122345/to-convert-string-to-variable-name
"""

from PySide.QtCore import Qt


def keyPressed(key, currentWidget):
    pass

class SettingsError(Exception):
    pass

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
            f.write("\nOTHER")
            self.writeSettingsFromOneDict(f, self.otherSettingsDict)
    
    def writeSettingsFromOneDict(self, f, dict):
        # just used in module writeSettingsToFile
        for i in dict:
            line = "\n" + i + " = "
            c = 1
            for v in dict[i]:
                if c > 1:
                    line += ", "
                line += v.replace("Key_","")
                c += 1
            f.write(line)
    
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


if __name__ == '__main__':
    settings = Settings()
    settings.setDefaultSettings()
    settings.writeSettingsToFile()
    
    print(settings.keySettingsDict)
    print(settings.otherSettingsDict)
    
    print("meaning for Qt.Key_S: ",settings.findKeyMeaning(Qt.Key_S))
    settings.checkIfKeysUsedByOtherSetting("MoveDown", ["Key_Up", "Key_9", "Key_Q", "Key_S"])
    
    