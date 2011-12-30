#!/usr/bin/env python

import unittest
from wish.p10.commands.away import AwayHandler

class StateDouble():
    
    def set_away(self, numeric, reason):
        self.change = "away"
        self.reason = reason
    
    def set_back(self, numeric):
        self.change = "back"
        self.reason = ""

class AwayTest(unittest.TestCase):
    
    def test_set_away_reason(self):
        s = StateDouble()
        c = AwayHandler(s)
        c.handle((1,1), ["I have gone away"])
        self.assertEquals("away", s.change)
        self.assertEquals("I have gone away", s.reason)
    
    def test_set_back_reason(self):
        s = StateDouble()
        c = AwayHandler(s)
        c.handle((1,1), [""])
        self.assertEquals("back", s.change)
    
    def test_set_back_no_reason(self):
        s = StateDouble()
        c = AwayHandler(s)
        c.handle((1,1), [])
        self.assertEquals("back", s.change)
    
    # No further unit tests required here - covered by test.p10.state

def main():
    unittest.main()

if __name__ == '__main__':
    main()
