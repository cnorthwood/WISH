#!/usr/bin/env python

import unittest
import p10.commands.clearmode

class StateDouble:
    
    removed_modes = []
    clearbanscalled = False
    clearopscalled = False
    clearvoicescalled = False
    
    def __init__(self):
        self.removed_modes = []
        self.clearbanscalled = False
        self.clearopscalled = False
        self.clearvoicescalled = False
    
    def changeChannelMode(self, origin, name, mode):
        self.removed_modes.append(mode[0][1])
    
    def clearChannelBans(self, origin, name):
        self.clearbanscalled = True
    
    def clearChannelOps(self, origin, name):
        self.clearopscalled = True
    
    def clearChannelVoices(self, origin, name):
        self.clearvoicescalled = True

class ClearModeTest(unittest.TestCase):
    
    def testNormalClear(self):
        s = StateDouble()
        c = p10.commands.clearmode.clearmode(s)
        c.handle((1,1), ["#test", "cNt"])
        self.assertEquals(['c','N','t'], s.removed_modes)
    
    def testBanClear(self):
        s = StateDouble()
        c = p10.commands.clearmode.clearmode(s)
        c.handle((1,1), ["#test", "b"])
        self.assertTrue(s.clearbanscalled)
        self.assertEquals([], s.removed_modes)
    
    def testOpClear(self):
        s = StateDouble()
        c = p10.commands.clearmode.clearmode(s)
        c.handle((1,1), ["#test", "o"])
        self.assertTrue(s.clearopscalled)
        self.assertEquals([], s.removed_modes)
    
    def testVoiceClear(self):
        s = StateDouble()
        c = p10.commands.clearmode.clearmode(s)
        c.handle((1,1), ["#test", "v"])
        self.assertTrue(s.clearvoicescalled)
        self.assertEquals([], s.removed_modes)
    
    # No further unit tests required here - covered by test.p10.state

def main():
    unittest.main()

if __name__ == '__main__':
    main()