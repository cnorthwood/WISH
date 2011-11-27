#!/usr/bin/env python

import unittest
import p10.commands.time

class StateDouble:
    
    insight = None
    maxClientNumerics = dict({1: 262143})
    
    def __init__(self):
        self.insight = None
    
    def requestTime(self, origin, target):
        self.insight = (origin, target)

class TimeTest(unittest.TestCase):
    
    def testCallbackCalled(self):
        s = StateDouble()
        a = p10.commands.time.time(s)
        a.handle((1,1), ["AB"])
        self.assertEquals(((1,1), (1, None)), s.insight)
    
def main():
    unittest.main()

if __name__ == '__main__':
    main()