#!/usr/bin/env python

import unittest
from wish.p10.commands.wallops import WallOpsHandler

class StateDouble():
    
    def __init__(self):
        self.insight = []
    
    def wallops(self, origin, message):
        self.insight.append((message))

class WallopsTest(unittest.TestCase):
    
    def test_wallops(self):
        s = StateDouble()
        c = WallOpsHandler(s)
        c.handle((1,1), ["Test"])
        self.assertEquals([("Test")], s.insight)
