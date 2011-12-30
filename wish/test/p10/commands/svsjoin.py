#!/usr/bin/env python

import unittest
from wish.p10.commands.svsjoin import SvsJoinHandler

class StateDouble():
    
    max_client_numerics = {1: 262143}
    
    def __init__(self):
        self.channel = []
    
    def join_channel(self, origin, numeric, name, modes, ts=0):
        self.channel.append((numeric, name, ts))


class SvsjoinTest(unittest.TestCase):
    
    def test_svsjoin(self):
        s = StateDouble()
        c = SvsJoinHandler(s)
        c.handle((1, None), ["ABAAB", "#foo"])
        self.assertEquals([((1,1), "#foo", 0)], s.channel)
    
    def test_svsjoin_multi(self):
        s = StateDouble()
        c = SvsJoinHandler(s)
        c.handle((1, None), ["ABAAB", "#foo,#bar"])
        self.assertEquals([((1,1), "#foo", 0), ((1,1), "#bar", 0)], s.channel)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
