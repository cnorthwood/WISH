#!/usr/bin/env python

import unittest
import p10.commands.links

class StateDouble:
    
    insight = None
    maxClientNumerics = dict({1: 262143})
    
    def __init__(self):
        self.insight = None
    
    def sendLinksInfo(self, origin, target, mask):
        self.insight = (origin, target, mask)

class LinksTest(unittest.TestCase):
    
    def testCallbackCalled(self):
        s = StateDouble()
        a = p10.commands.links.links(s)
        a.handle((1,1), ["AB", "*.example.com"])
        self.assertEquals(((1,1), (1, None), "*.example.com"), s.insight)
    
def main():
    unittest.main()

if __name__ == '__main__':
    main()