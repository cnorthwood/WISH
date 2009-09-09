#!/usr/bin/env python

import unittest
import p10.commands.names

class StateDouble:
    
    insight = None
    maxClientNumerics = dict({1: 262143})
    
    def __init__(self):
        self.insight = None
    
    def requestChannelUsers(self, origin, target, channels):
        self.insight = (origin, target, channels)

class NamesTest(unittest.TestCase):
    
    def testCallbackCalled(self):
        s = StateDouble()
        a = p10.commands.names.names(s)
        a.handle((1,1), ["#test", "AB"])
        self.assertEquals(((1,1), (1, None), ["#test"]), s.insight)
    
    def testCallbackCalledMulti(self):
        s = StateDouble()
        a = p10.commands.names.names(s)
        a.handle((1,1), ["#test,#foo", "AB"])
        self.assertEquals(((1,1), (1, None), ["#test","#foo"]), s.insight)
    
def main():
    unittest.main()

if __name__ == '__main__':
    main()