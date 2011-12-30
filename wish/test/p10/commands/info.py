#!/usr/bin/env python

import unittest

from wish.p10.commands.info import InfoHandler

class StateDouble():
    
    max_client_numerics = {1: 262143}
    
    def __init__(self):
        self.insight = None
    
    def request_server_info(self, origin, target):
        self.insight = (origin, target)


class InfoTest(unittest.TestCase):
    
    def test_triggers_callback(self):
        s = StateDouble()
        a = InfoHandler(s)
        a.handle((1,1), ["AB"])
        self.assertEquals(((1,1), (1, None)), s.insight)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
