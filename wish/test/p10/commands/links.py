#!/usr/bin/env python

import unittest
from wish.p10.commands.links import LinksHandler

class StateDouble():
    
    max_client_numerics = {1: 262143}
    
    def __init__(self):
        self.insight = None
    
    def request_links(self, origin, target, mask):
        self.insight = (origin, target, mask)


class LinksTest(unittest.TestCase):
    
    def testCallbackCalled(self):
        s = StateDouble()
        a = LinksHandler(s)
        a.handle((1,1), ["AB", "*.example.com"])
        self.assertEquals(((1,1), (1, None), "*.example.com"), s.insight)
    
def main():
    unittest.main()

if __name__ == '__main__':
    main()
