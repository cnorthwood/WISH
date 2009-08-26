#!/usr/bin/env python

import unittest
import p10.commands.stats

class StateDouble:
    
    insight = None
    maxClientNumerics = dict({1: 262143})
    
    def __init__(self):
        self.insight = None
    
    def requestStats(self, origin, target, stat, arg):
        self.insight = (origin, target, stat, arg)

class StatsTest(unittest.TestCase):
    
    def testCallbackCalledSimple(self):
        s = StateDouble()
        a = p10.commands.stats.stats(s)
        a.handle((1,1), ["B", "AB"])
        self.assertEquals(((1,1), (1, None), "B", None), s.insight)
    
    def testCallbackCalledArg(self):
        s = StateDouble()
        a = p10.commands.stats.stats(s)
        a.handle((1,1), ["D", "AB", "*.example.com"])
        self.assertEquals(((1,1), (1, None), "D", "*.example.com"), s.insight)
    
def main():
    unittest.main()

if __name__ == '__main__':
    main()