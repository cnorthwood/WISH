#!/usr/bin/env python

import unittest
import p10.commands.wallops

class StateDouble:
    insight = []
    def __init__(self):
        self.insight = []
    def wallops(self, origin, message):
        self.insight.append((message))

class WallopsTest(unittest.TestCase):
    
    def testWallops(self):
        s = StateDouble()
        c = p10.commands.wallops.wallops(s)
        c.handle((1,1), ["Test"])
        self.assertEquals([("Test")], s.insight)