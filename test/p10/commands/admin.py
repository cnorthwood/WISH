#!/usr/bin/env python

import unittest
import p10.commands.admin

class StateDouble:
    
    insight = None
    maxClientNumerics = dict({1: 262143})
    
    def __init__(self):
        self.insight = None
    
    def requestAdminInfo(self, origin, target):
        self.insight = (origin, target)

class AdminTest(unittest.TestCase):
    
    def testCallbackCalled(self):
        s = StateDouble()
        a = p10.commands.admin.admin(s)
        a.handle((1,1), ["AB"])
        self.assertEquals(((1,1), (1, None)), s.insight)
    
def main():
    unittest.main()

if __name__ == '__main__':
    main()