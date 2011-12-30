#!/usr/bin/env python

import unittest
from wish.p10.commands.silence import SilenceHandler

class StateDouble():
    
    def __init__(self):
        self.insight = []
    
    def add_silence(self, numeric, mask):
        self.insight.append(('add', mask))
    
    def remove_silence(self, numeric, mask):
        self.insight.append(('remove', mask))


class SilenceTest(unittest.TestCase):
    
    def test_add_silence(self):
        s = StateDouble()
        c = SilenceHandler(s)
        c.handle((1,1), ["ABAAB", "foo!bar@example.com"])
        self.assertEquals([('add', 'foo!bar@example.com')], s.insight)
    
    def test_del_silence(self):
        s = StateDouble()
        c = SilenceHandler(s)
        c.handle((1,1), ["ABAAB", "-foo!bar@example.com"])
        self.assertEquals([('remove', 'foo!bar@example.com')], s.insight)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
