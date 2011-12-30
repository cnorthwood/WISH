#!/usr/bin/env python

import unittest

from wish.p10.commands.clearmode import ClearModeHandler

class StateDouble():
    
    def __init__(self):
        self.removed_modes = []
        self.clearbanscalled = False
        self.clearopscalled = False
        self.clearvoicescalled = False
    
    def change_channel_mode(self, origin, name, modes):
        for mode in modes:
            self.removed_modes.append(mode[0][1])
    
    def clear_channel_bans(self, origin, name):
        self.clearbanscalled = True
    
    def clear_channel_ops(self, origin, name):
        self.clearopscalled = True
    
    def clear_channel_voices(self, origin, name):
        self.clearvoicescalled = True

class ClearModeTest(unittest.TestCase):
    
    def test_normal_clear(self):
        s = StateDouble()
        c = ClearModeHandler(s)
        c.handle((1,1), ["#test", "cNt"])
        self.assertEquals(['c','N','t'], s.removed_modes)
    
    def test_ban_clear(self):
        s = StateDouble()
        c = ClearModeHandler(s)
        c.handle((1,1), ["#test", "b"])
        self.assertTrue(s.clearbanscalled)
        self.assertEquals([], s.removed_modes)
    
    def test_op_clear(self):
        s = StateDouble()
        c = ClearModeHandler(s)
        c.handle((1,1), ["#test", "o"])
        self.assertTrue(s.clearopscalled)
        self.assertEquals([], s.removed_modes)
    
    def test_voice_clear(self):
        s = StateDouble()
        c = ClearModeHandler(s)
        c.handle((1,1), ["#test", "v"])
        self.assertTrue(s.clearvoicescalled)
        self.assertEquals([], s.removed_modes)
    
    # No further unit tests required here - covered by test.p10.state

def main():
    unittest.main()

if __name__ == '__main__':
    main()
