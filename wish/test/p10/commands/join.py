#!/usr/bin/env python

import unittest
from wish.p10.commands.join import JoinHandler

class StateDouble():
    
    def __init__(self):
        self.channel = ""
    
    def join_channel(self, origin, numeric, name, modes, ts=0):
        self.channel = (name, ts)
    
    def part_all_channels(self, numeric):
        self.channel = "partall"


class JoinTest(unittest.TestCase):
    
    def test_join(self):
        s = StateDouble()
        c = JoinHandler(s)
        c.handle((1,1), ["#foo", "81"])
        self.assertEquals(("#foo", 81), s.channel)
        
    def test_join_no_ts(self):
        s = StateDouble()
        c = JoinHandler(s)
        c.handle((1,1), ["#foo"])
        self.assertEquals(("#foo", 1270080000), s.channel)
    
    def test_part_all(self):
        s = StateDouble()
        c = JoinHandler(s)
        c.handle((1,1), ["0"])
        self.assertEquals("partall", s.channel)
    
    # No further unit tests required here - covered by test.p10.state


def main():
    unittest.main()

if __name__ == '__main__':
    main()
