#!/usr/bin/env python

import unittest
from wish.p10.commands.time import TimeHandler

class StateDouble():
    
    max_client_numerics = {1: 262143}
    
    def __init__(self):
        self.insight = None
    
    def request_time(self, origin, target):
        self.insight = (origin, target)


class TimeTest(unittest.TestCase):
    
    def test_callback_called(self):
        s = StateDouble()
        a = TimeHandler(s)
        a.handle((1,1), ["AB"])
        self.assertEquals(((1,1), (1, None)), s.insight)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
