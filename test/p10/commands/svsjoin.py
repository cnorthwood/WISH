#!/usr/bin/env python

import unittest
import p10.commands.join

class StateDouble:
    channel = []
    maxClientNumerics = dict({1: 262143})
    def __init__(self):
        self.channel = []
    def joinChannel(self, origin, numeric, name, modes, ts=0):
        self.channel.append((numeric, name, ts))

class SvsjoinTest(unittest.TestCase):
    
    def testSvsjoin(self):
        s = StateDouble()
        c = p10.commands.svsjoin.svsjoin(s)
        c.handle((1, None), ["ABAAB", "#foo"])
        self.assertEquals([((1,1), "#foo", 0)], s.channel)
    
    def testSvsjoinMultiy(self):
        s = StateDouble()
        c = p10.commands.svsjoin.svsjoin(s)
        c.handle((1, None), ["ABAAB", "#foo,#bar"])
        self.assertEquals([((1,1), "#foo", 0), ((1,1), "#bar", 0)], s.channel)

def main():
    unittest.main()

if __name__ == '__main__':
    main()