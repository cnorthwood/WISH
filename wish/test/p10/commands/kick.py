#!/usr/bin/env python

import unittest
from wish.p10.commands.kick import KickHandler

class StateDouble():
    
    max_client_numerics = {1: 262143}
    
    def __init__(self):
        self.insight = None
    
    def kick(self, origin, channel, target, reason):
        self.insight = (channel, target, reason)


class KickTest(unittest.TestCase):
    
    def testKickCalled(self):
        s = StateDouble()
        c = KickHandler(s)
        c.handle((1, 1), ["#test", "ABAAC", "Fun"])
        self.assertEquals(('#test', (1,2), "Fun"), s.insight)
    
    # No further unit tests required here - covered by test.p10.state


def main():
    unittest.main()

if __name__ == '__main__':
    main()
