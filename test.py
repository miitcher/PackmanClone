"""
    Handles unittests.
    Documentation:
        https://docs.python.org/3.4/library/unittest.html
"""

import unittest
from ui import Settings, SettingsError
from PySide.QtCore import Qt

class TestSettingsMethods(unittest.TestCase):
    
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
        expectedStrList = ['# SETTINGS\n', 'KEYS\n', 'MoveDown = Down, S\n', 'MoveRight = Right, D\n', 'Pause = 9, C\n', 'Esc = Escape\n', 'MoveUp = Up, W\n', 'MoveLeft = Left, A\n', 'OTHER\n', 'Resolution = 1280x720\n', 'WindowMode = Windowed\n', 'MenuScale = 0.75\n']
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
        defaultOtherSettingsDict = {'MenuScale': ['0.75'], 'Resolution': ['1280x720'], 'WindowMode': ['Windowed']}
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
        expectedOtherSettingsDict = {'MenuScale': ['0.75'], 'Resolution': ['1280x720'], 'WindowMode': ['Windowed']}
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


if __name__ == '__main__':
    unittest.main()