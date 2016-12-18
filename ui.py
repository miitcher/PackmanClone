"""
    Handles users inputs and settings.
    
    Maby usefull:
        http://stackoverflow.com/questions/19122345/to-convert-string-to-variable-name
"""

from PySide.QtCore import Qt


def keyPressed(key, currentWidget):
    pass

class Settings():
    def __init__(self):
        self.readSettings()
        self.printDict()
    
    def printDict(self):
        print(self.settingDict)
    
    def readSettings(self):
        self.settingDict = {}
        with open("settings.ini", "r") as f:
            line = f.readline()
            while line != "":
                line = line.strip()
                if line[0] != "#":
                    try:
                        [setting, kstr] = line.split("=")
                        setting = setting.strip()
                        keysPre = kstr.split(",")
                        keys = []
                        for k in keysPre:
                            k = "Qt.Key_" + k.strip()
                            print(type(k),k)
                            exec("key = %s" % (k))
                            # meh meh: could compare strings or get
                            # the exec-command to work
                            print(type(key),key)
                            
                            keys.append(k)
                        self.settingDict[setting] = keys
                    except ValueError:
                        print("Error. UI. Line in setting.ini is in wrong format. Will be skipped.")
                line = f.readline()
    
    def setDefaultSettings(self):
        # creates the "settings.ini"-file, or overwrites it if it exists
        with open("settings.ini", "w") as f:
            f.write(
    "# SETTINGS\n\
    MoveUp = Up\n\
    MoveDown = Down, S\n\
    jees = Right")
    
    def changeSetting(self, setting, val):
        settingDict = readSettings()
        settingDict[setting] = val
        print(settingDict)


if __name__ == '__main__':
    settings = Settings()
    #print(readSettings())
    #settings.setDefaultSettings()
    #changeSetting("jees", Qt.Key_T)
    