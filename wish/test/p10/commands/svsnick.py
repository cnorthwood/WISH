#!/usr/bin/env python

import unittest
from wish.p10.commands.svsnick import SvsNickHandler

class StateDouble():
    
    max_client_numerics = {1: 262143}
    
    def __init__(self):
        self.insight = []
    
    @property
    def ts(self):
        return 18
    
    def change_nick(self, origin, numeric, newnick, newts):
        self.insight.append((numeric, newnick, newts))


class SvsnickTest(unittest.TestCase):
    
    def test_nick_change(self):
        s = StateDouble()
        c = SvsNickHandler(s)
        c.handle((1,1), ['ABAAC', 'newnick'])
        self.assertEquals([((1,2), "newnick", 18)], s.insight)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
