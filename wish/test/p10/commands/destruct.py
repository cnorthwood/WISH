#!/usr/bin/env python

import unittest

from wish.p10.commands.destruct import DestructHandler

class StateDouble():
    
    def __init__(self):
        self.insight = None
    
    def destroy_channel(self, origin, channel, ts):
        self.insight = (channel, ts)


class DestructTest(unittest.TestCase):
    
    def testDestroyCalled(self):
        s = StateDouble()
        c = DestructHandler(s)
        c.handle((1, None), ["#test", "17"])
        self.assertEquals(('#test', 17), s.insight)
    
    # No further unit tests required here - covered by test.p10.state


def main():
    unittest.main()

if __name__ == '__main__':
    main()
