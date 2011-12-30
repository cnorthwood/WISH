#!/usr/bin/env python

import unittest
from wish.p10.commands.wallchops import WallChOpsHandler

class StateDouble():
    
    def __init__(self):
        self.insight = []
        
    def wallchops(self, origin, channel, message):
        self.insight.append((channel, message))

class WallchopsTest(unittest.TestCase):
    
    def test_wallchops(self):
        s = StateDouble()
        c = WallChOpsHandler(s)
        c.handle((1,1), ["#test", "Test"])
        self.assertEquals([("#test", "Test")], s.insight)
