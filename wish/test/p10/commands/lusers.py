#!/usr/bin/env python

import unittest
from wish.p10.commands.lusers import LusersHandler

class StateDouble():
    
    max_client_numerics = {1: 262143}
    
    def __init__(self):
        self.insight = None
    
    def request_lusers(self, origin, target, dummy):
        self.insight = (origin, target, dummy)


class LusersTest(unittest.TestCase):
    
    def testCallbackCalled(self):
        s = StateDouble()
        a = LusersHandler(s)
        a.handle((1,1), ["dummy", "AB"])
        self.assertEquals(((1,1), (1, None), "dummy"), s.insight)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
