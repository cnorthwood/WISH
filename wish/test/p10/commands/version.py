#!/usr/bin/env python

import unittest
from wish.p10.commands.version import VersionHandler

class StateDouble():
    
    max_client_numerics = {1: 262143}
    
    def __init__(self):
        self.insight = None
    
    def request_version(self, origin, target):
        self.insight = (origin, target)

class VersionTest(unittest.TestCase):
    
    def testCallbackCalled(self):
        s = StateDouble()
        a = VersionHandler(s)
        a.handle((1,1), ["AB"])
        self.assertEquals(((1,1), (1, None)), s.insight)
    
def main():
    unittest.main()

if __name__ == '__main__':
    main()
