#!/usr/bin/env python

import unittest
import p10.commands.join

class StateDouble:
    channel = ""
    def __init__(self):
        self.channel = ""
    def joinChannel(self, origin, numeric, name, modes, ts=0):
        self.channel = (name, ts)
    def partAllChannels(self, numeric):
        self.channel = "partall"

class JoinTest(unittest.TestCase):
    
    def testJoin(self):
        s = StateDouble()
        c = p10.commands.join.join(s)
        c.handle((1,1), ["#foo", "81"])
        self.assertEquals(("#foo", 81), s.channel)
        
    def testJoinNoTS(self):
        s = StateDouble()
        c = p10.commands.join.join(s)
        c.handle((1,1), ["#foo"])
        self.assertEquals(("#foo", 1270080000), s.channel)
    
    def testPartAll(self):
        s = StateDouble()
        c = p10.commands.join.join(s)
        c.handle((1,1), ["0"])
        self.assertEquals("partall", s.channel)
    
    # No further unit tests required here - covered by test.p10.state

def main():
    unittest.main()

if __name__ == '__main__':
    main()