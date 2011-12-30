#!/usr/bin/env python

import unittest
from wish.p10.commands.part import PartHandler

class StateDouble():
    
    def __init__(self):
        self.insight = []
    
    def part_channel(self, numeric, name, reason):
        self.insight.append((name, reason))


class PartTest(unittest.TestCase):
    
    def test_single_part(self):
        s = StateDouble()
        c = PartHandler(s)
        c.handle((1,1), ["#test", "Reason"])
        self.assertEquals([("#test", "Reason")], s.insight)
    
    def test_multi_part(self):
        s = StateDouble()
        c = PartHandler(s)
        c.handle((1,1), ["#test,#foo", "Reason"])
        self.assertEquals([("#test", "Reason"), ("#foo", "Reason")], s.insight)

 
def main():
    unittest.main()

if __name__ == '__main__':
    main()
