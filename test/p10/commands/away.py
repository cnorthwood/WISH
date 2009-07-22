#!/usr/bin/env python

import unittest
import p10.commands.away

class StateDouble:
    change = ""
    reason = ""
    def setAway(self, numeric, reason, local):
        self.change = "away"
        self.reason = reason
    
    def setBack(self, numeric, local):
        self.change = "back"
        self.reason = ""

class AwayTest(unittest.TestCase):
    
    def testSetAwayReason(self):
        s = StateDouble()
        c = p10.commands.away.away(s)
        c.handle((1,1), ["I have gone away"])
        self.assertEquals("away", s.change)
        self.assertEquals("I have gone away", s.reason)
    
    def testSetBackReason(self):
        s = StateDouble()
        c = p10.commands.away.away(s)
        c.handle((1,1), [""])
        self.assertEquals("back", s.change)
    
    def testSetBackNoReason(self):
        s = StateDouble()
        c = p10.commands.away.away(s)
        c.handle((1,1), [])
        self.assertEquals("back", s.change)
    
    # No further unit tests required here - covered by test.p10.state

def main():
    unittest.main()

if __name__ == '__main__':
    main()