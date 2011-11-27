#!/usr/bin/env python

import unittest
import p10.commands.part

class StateDouble:
    insight = []
    def __init__(self):
        self.insight = []
    def partChannel(self, numeric, name, reason):
        self.insight.append((name, reason))

class PartTest(unittest.TestCase):
    
    def testSinglePart(self):
        s = StateDouble()
        c = p10.commands.part.part(s)
        c.handle((1,1), ["#test", "Reason"])
        self.assertEquals([("#test", "Reason")], s.insight)
    
    def testMultiPart(self):
        s = StateDouble()
        c = p10.commands.part.part(s)
        c.handle((1,1), ["#test,#foo", "Reason"])
        self.assertEquals([("#test", "Reason"), ("#foo", "Reason")], s.insight)
    
def main():
    unittest.main()

if __name__ == '__main__':
    main()