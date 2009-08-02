#!/usr/bin/env python

import unittest
import p10.commands.kick

class StateDouble:
    insight = None
    maxClientNumerics = dict({1: 262143})
    def __init__(self):
        self.insight = None
    def kick(self, origin, channel, target, reason):
        self.insight = (channel, target, reason)

class KickTest(unittest.TestCase):
    
    def testKickCalled(self):
        s = StateDouble()
        c = p10.commands.kick.kick(s)
        c.handle((1, 1), ["#test", "ABAAC", "Fun"])
        self.assertEquals(('#test', (1,2), "Fun"), s.insight)
    
    # No further unit tests required here - covered by test.p10.state

def main():
    unittest.main()

if __name__ == '__main__':
    main()