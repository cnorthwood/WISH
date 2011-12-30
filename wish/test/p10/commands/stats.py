#!/usr/bin/env python

import unittest
from wish.p10.commands.stats import StatsHandler

class StateDouble():
    
    max_client_numerics = {1: 262143}
    
    def __init__(self):
        self.insight = None
    
    def request_stats(self, origin, target, stat, arg):
        self.insight = (origin, target, stat, arg)


class StatsTest(unittest.TestCase):
    
    def test_callback_called_simple(self):
        s = StateDouble()
        a = StatsHandler(s)
        a.handle((1,1), ["B", "AB"])
        self.assertEquals(((1,1), (1, None), "B", None), s.insight)
    
    def test_callback_called_arg(self):
        s = StateDouble()
        a = StatsHandler(s)
        a.handle((1,1), ["D", "AB", "*.example.com"])
        self.assertEquals(((1,1), (1, None), "D", "*.example.com"), s.insight)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
