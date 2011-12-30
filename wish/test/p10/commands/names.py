#!/usr/bin/env python

import unittest
from wish.p10.commands.names import NamesHandler

class StateDouble():
    
    max_client_numerics = {1: 262143}
    
    def __init__(self):
        self.insight = None
    
    def request_channel_users(self, origin, target, channels):
        self.insight = (origin, target, channels)


class NamesTest(unittest.TestCase):
    
    def test_callback_called(self):
        s = StateDouble()
        a = NamesHandler(s)
        a.handle((1,1), ["#test", "AB"])
        self.assertEquals(((1,1), (1, None), ["#test"]), s.insight)
    
    def test_callback_called_multi(self):
        s = StateDouble()
        a = NamesHandler(s)
        a.handle((1,1), ["#test,#foo", "AB"])
        self.assertEquals(((1,1), (1, None), ["#test","#foo"]), s.insight)
    
def main():
    unittest.main()

if __name__ == '__main__':
    main()
