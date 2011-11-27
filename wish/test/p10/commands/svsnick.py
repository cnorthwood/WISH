#!/usr/bin/env python

import unittest
import p10.commands.nick

class StateDouble:
    insight = []
    maxClientNumerics = dict({1: 262143})
    def __init__(self):
        self.insight = []
    def ts(self):
        return 18
    def changeNick(self, origin, numeric, newnick, newts):
        self.insight.append((numeric, newnick, newts))

class SvsnickTest(unittest.TestCase):
    
    def testNickChange(self):
        s = StateDouble()
        c = p10.commands.svsnick.svsnick(s)
        c.handle((1,1), ['ABAAC', 'newnick'])
        self.assertEquals([((1,2), "newnick", 18)], s.insight)

def main():
    unittest.main()

if __name__ == '__main__':
    main()