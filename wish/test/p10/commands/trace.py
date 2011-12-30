#!/usr/bin/env python

import unittest
from wish.p10.commands.trace import TraceHandler

class StateDouble():
    
    max_client_numerics = {1: 262143}
    
    def __init__(self):
        self.insight = None
    
    def trace(self, origin, search, target):
        self.insight = (origin, search, target)


class TraceTest(unittest.TestCase):
    
    def test_callback_called(self):
        s = StateDouble()
        a = TraceHandler(s)
        a.handle((1,1), ["test.example.com", "AB"])
        self.assertEquals(((1,1), "test.example.com", (1, None)), s.insight)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
