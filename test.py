"""
    Handles unittests.
    Documentation:
        https://docs.python.org/3.4/library/unittest.html
"""

from ui import *
from bodies import *
from main import *
from graphics import *
from physics import *

import unittest, shutil, os, sys

from PySide.QtCore import Qt


class TestSettingsMethods(unittest.TestCase):
    # ui.py
    def test_initSettings(self):
        s = Settings()
        s.keySettingsDict = {"Pause":["Key_0"]}
        s.otherSettingsDict = {}
        self.assertTrue(s.keySettingsDict)
        self.assertFalse(s.otherSettingsDict)
    
    def test_getSettingsFromFile(self):
        s = Settings()
        s.setDefaultSettings()
        # make the settings.ini-file have wrong format
        with open("settings.ini", "a") as f:
            f.write("\nduck")
        with self.assertRaises(SettingsError):
            s2 = Settings()
        # write a regular settings.ini-file
        with open("settings.ini", "w") as f:
            f.write("# SETTINGS\nKEYS\nMoveRight = U, I")
        s.getSettingsFromFile()
        expectedKeySettingsDict = {'MoveRight': ['Key_U', 'Key_I']}
        expectedOtherSettingsDict = {}
        self.assertEqual(s.keySettingsDict, expectedKeySettingsDict)
        self.assertEqual(s.otherSettingsDict, expectedOtherSettingsDict)
    
    def test_writeSettingsToFile(self):
        s = Settings()
        s.setDefaultSettings()
        s.keySettingsDict["Pause"] = ["Key_9", "Key_C"]
        s.writeSettingsToFile()
        with open("settings.ini", "r") as f:
            strList = f.readlines()
        expectedStrList = ['# SETTINGS\n', 'KEYS\n', 'MoveDown = Down, S\n', 'MoveRight = Right, D\n', 'Pause = 9, C\n', 'Esc = Escape\n', 'MoveUp = Up, W\n', 'MoveLeft = Left, A\n', 'OTHER\n', 'Resolution = 1280x720\n', 'WindowMode = Windowed\n', 'MenuScale = 0.75\n', 'FPS = 60\n']
        self.assertEqual(strList[0], expectedStrList[0])
        self.assertEqual(strList[1], expectedStrList[1])
        self.assertEqual(strList[8], expectedStrList[8])
        for row in strList:
            if row[-1] != '\n':
                row += '\n'
            self.assertTrue(row in expectedStrList)
    
    def test_setDefaultSettings(self):
        s = Settings()
        s.keySettingsDict = {"MoveDown":["Key_8","Key_P"]}
        s.otherSettingsDict = {"Resolution":["200x400"]}
        s.setDefaultSettings()
        defaultKeySettingsDict = {'MoveUp': ['Key_Up', 'Key_W'], 'Esc': ['Key_Escape'], 'Pause': ['Key_Space'], 'MoveDown': ['Key_Down', 'Key_S'], 'MoveRight': ['Key_Right', 'Key_D'], 'MoveLeft': ['Key_Left', 'Key_A']}
        defaultOtherSettingsDict = {'MenuScale': ['0.75'], 'Resolution': ['1280x720'], 'WindowMode': ['Windowed'], 'FPS': ['60']}
        self.assertEqual(s.keySettingsDict, defaultKeySettingsDict)
        self.assertEqual(s.otherSettingsDict, defaultOtherSettingsDict)
        # testing empty setting dictionaries
        s.keySettingsDict = {}
        s.otherSettingsDict = {}
        s.setDefaultSettings()
        self.assertEqual(s.keySettingsDict, defaultKeySettingsDict)
        self.assertEqual(s.otherSettingsDict, defaultOtherSettingsDict)
    
    def test_checkIfKeysUsedByOtherSetting(self):
        s = Settings()
        s.setDefaultSettings()
        s.keySettingsDict["Pause"] = ["Key_W","Key_S"]
        usedKeysDict1 = s.checkIfKeysUsedByOtherSetting("MoveLeft", ["Key_S","Key_Down","Key_H"])
        usedKeysDict2 = s.checkIfKeysUsedByOtherSetting("MoveUp", ["Key_9"])
        expectedUsedKeysDict1 = {'MoveDown': ['Key_Down', 'Key_S'], 'Pause': ['Key_S']}
        expectedUsedKeysDict2 = None
        self.assertEqual(usedKeysDict1, expectedUsedKeysDict1)
        self.assertEqual(usedKeysDict2, expectedUsedKeysDict2)
    
    def test_unassignKeysForSettings(self):
        s = Settings()
        s.setDefaultSettings()
        with self.assertRaises(ValueError):
            s.unassignKeysForSettings({"Pause":["Key_8"]})
        
        s.unassignKeysForSettings({"MoveUp":["Key_W"], "MoveDown":['Key_Down', 'Key_S'], "Esc":["Key_Escape"]})
        expectedKeySettingsDict = {'MoveUp': ['Key_Up'], 'Pause': ['Key_Space'], 'MoveRight': ['Key_Right', 'Key_D'], 'MoveLeft': ['Key_Left', 'Key_A'], 'MoveDown': [], 'Esc': []}
        expectedOtherSettingsDict = {'MenuScale': ['0.75'], 'Resolution': ['1280x720'], 'WindowMode': ['Windowed'], 'FPS': ['60']}
        self.assertEqual(s.keySettingsDict, expectedKeySettingsDict)
        self.assertEqual(s.otherSettingsDict, expectedOtherSettingsDict)
    
    def test_findKeyMeaning(self):
        s = Settings()
        s.setDefaultSettings()
        key1 = Qt.Key_Right
        key2 = Qt.Key_S
        key3 = Qt.Key_H
        expected1 = "MoveRight"
        expected2 = "MoveDown"
        expected3 = None
        self.assertEqual(s.findKeyMeaning(key1), expected1)
        self.assertEqual(s.findKeyMeaning(key2), expected2)
        self.assertEqual(s.findKeyMeaning(key3), expected3)
    
    def test_getSettings(self):
        """
        getGeneral
        getResolution
        getFPS
        getMenuScale
        getWindowMode
        """
        s = Settings()
        s.setDefaultSettings()
        defaultValue = "default_88"
        FPSValue = 144
        # usual usecase
        s.keySettingsDict["FPS"] = [str(FPSValue)]
        self.assertEqual(s.getGeneral("FPS", defaultValue), 60)
        self.assertEqual(s.getResolution(), (1280,720))
        self.assertEqual(s.getFPS(), 60)
        self.assertEqual(s.getMenuScale(), 0.75)
        self.assertEqual(s.getWindowMode(), "Windowed")
        # breaking
        with self.assertRaises(SettingsError):
            s.getGeneral("NotASetting", defaultValue)

class TestBodies(unittest.TestCase):
    # bodies.py
    def test_Body(self):
        app = QApplication(sys.argv)
        mw = MainWindow()
        mw.settings.setDefaultSettings()
        mw.processSettingsChanged()
        
        x0 = 3
        y0 = 5
        size = 1 # default value
        x = x0 - size/2
        y = y0 - size/2
        
        b = Body(mw, (x0,y0))
        # str
        self.assertEqual(str(b), "(%s, %s)" % (x,y))
        # Hitbox
        expectedHBList = [x, x + size, y, y + size]
        self.assertEqual(b.HBList, expectedHBList)
        
        speed = 2
        change = 1/60 * speed
        b.direction = UP
        b.speed = speed
        # move
        b.move()
        self.assertEqual(str(b), "(%s, %s)" % (x,y-change))
        expectedHBList[UP] -= change
        expectedHBList[DOWN] -= change
        self.assertEqual(b.HBList, expectedHBList)
    
    def test_Pacman(self):
        pass


if __name__ == '__main__':
    """
    We copy the settings.ini file and use
    the old file, so the users changed settings
    does not dissapear.
    The lines after the "unittest.main()"-line
    will not be executed.
    """
    if not os.path.isfile("settings_BACKUP.ini"):
        shutil.copyfile("settings.ini", "settings_BACKUP.ini")
        print('Backup of "settings.ini" created as file: "settings_BACKUP.ini".')
    unittest.main()