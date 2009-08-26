#!/usr/bin/env python

import unittest
import p10.commands.trace

class StateDouble:
    
    insight = None
    maxClientNumerics = dict({1: 262143})
    
    def __init__(self):
        self.insight = None
    
    def trace(self, origin, search, target):
        self.insight = (origin, search, target)

class TraceTest(unittest.TestCase):
    
    def testCallbackCalled(self):
        s = StateDouble()
        a = p10.commands.trace.trace(s)
        a.handle((1,1), ["test.example.com", "AB"])
        self.assertEquals(((1,1), "test.example.com", (1, None)), s.insight)
    
def main():
    unittest.main()

if __name__ == '__main__':
    main()