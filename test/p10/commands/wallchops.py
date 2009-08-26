#!/usr/bin/env python

import unittest
import p10.commands.wallchops

class StateDouble:
    insight = []
    def __init__(self):
        self.insight = []
    def wallchops(self, origin, channel, message):
        self.insight.append((channel, message))

class WallchopsTest(unittest.TestCase):
    
    def testWallchops(self):
        s = StateDouble()
        c = p10.commands.wallchops.wallchops(s)
        c.handle((1,1), ["#test", "Test"])
        self.assertEquals([("#test", "Test")], s.insight)