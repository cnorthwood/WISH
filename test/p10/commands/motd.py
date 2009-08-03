#!/usr/bin/env python

import unittest
import p10.commands.motd

class StateDouble:
    
    insight = None
    maxClientNumerics = dict({1: 262143})
    
    def __init__(self):
        self.insight = None
    
    def sendMOTD(self, origin, target):
        self.insight = (origin, target)

class MOTDTest(unittest.TestCase):
    
    def testCallbackCalled(self):
        s = StateDouble()
        a = p10.commands.motd.motd(s)
        a.handle((1,1), ["AB"])
        self.assertEquals(((1,1), (1, None)), s.insight)
    
def main():
    unittest.main()

if __name__ == '__main__':
    main()