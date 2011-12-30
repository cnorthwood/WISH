#!/usr/bin/env python

import unittest

from wish.irc.motd import MotdResponder
from wish.irc.state import User, Server, Channel

class StateDouble():
    
    def __init__(self):
        self.insight = []
        self.max_client_numerics = {1: 262143}
        self.users = {
            (1,1): User((1,1), "test", "test", "example.com", [], 6, 0,
                1234, "Joe Bloggs")
        }
        self.servers = {
            1: Server(None, 1, "test.example.com", 1234, 1234, 1234, "P10", 0,
                      [], "A test description")
        }
        self.channels = {
            "#test": Channel("#test", 1234)
        }
    
    @property
    def server_id(self):
        return 1
    
    def oobmsg(self, origin, target, type, args):
        self.insight.append((origin, type, target, args))
        
    CALLBACK_REQUESTMOTD = "RequestMOTD"
    def register_callback(self, type, callbackfn):
        pass
    
    @property
    def server_name(self):
        return "test.example.com"
    
    def numeric2nick(self, numeric):
        if numeric == (1, None):
            return "test.example.com"
        elif numeric == (2, None):
            return "test2.example.com"
        elif numeric == (3, None):
            return "test3.example.com"
        elif numeric == (1,6):
            return "localtest"
        elif numeric == (3, 2):
            return "test"


class IrcMotdTest(unittest.TestCase):
    
    def test_motd__reply(self):
        s = StateDouble()
        c = MotdResponder(s)
        c.callback_motd((3,6), (1, None))
        self.assertEquals([((1,None), "375", (3,6), ["test.example.com Message of the Day"]), ((1,None), "376", (3,6), ["End of /MOTD."])], s.insight)
    
    def test_motd_reply_if_relevant(self):
        s = StateDouble()
        c = MotdResponder(s)
        c.callback_motd((7,6), (2, None))
        self.assertEquals([], s.insight)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
