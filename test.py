"""
    Handles unittests.
    Documentation:
        https://docs.python.org/3.4/library/unittest.html
"""

import unittest
from ui import Settings

class TestSettingsMethods(unittest.TestCase):
    
    def test_initSettings(self):
        s = Settings()
        self.assertTrue(s.keySettingsDict)
        self.assertTrue(s.otherSettingsDict)
    
    def test_changeingAndAddingSettings(self):
        """
        Tests methods:
            changeKeySettings,
            changeOtherSettings,
            addKeyToKeySettings
        """
        s = Settings()
    
    def test_unasignKeysForOtherSettings(self):
        s = Settings()
    
    def test_setDefaultSettings(self):
        s = Settings()
    
    def test_getSettingsFromFile(self):
        s = Settings()
    
    def test_writeSettingsToFile(self):
        s = Settings()
    
    def test_findKeyMeaning(self):
        s = Settings()


if __name__ == '__main__':
    unittest.main()