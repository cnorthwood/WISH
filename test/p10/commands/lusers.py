#!/usr/bin/env python

import unittest
import p10.commands.lusers

class StateDouble:
    
    insight = None
    maxClientNumerics = dict({1: 262143})
    
    def __init__(self):
        self.insight = None
    
    def sendLusersInfo(self, origin, target, dummy):
        self.insight = (origin, target, dummy)

class LusersTest(unittest.TestCase):
    
    def testCallbackCalled(self):
        s = StateDouble()
        a = p10.commands.lusers.lusers(s)
        a.handle((1,1), ["dummy", "AB"])
        self.assertEquals(((1,1), (1, None), "dummy"), s.insight)
    
def main():
    unittest.main()

if __name__ == '__main__':
    main()