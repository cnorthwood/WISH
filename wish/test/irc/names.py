#!/usr/bin/env python

import unittest

from wish.irc.names import NamesResponder
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
    
    @property
    def server_name(self):
        return "test.example.com"
    
    def oobmsg(self, origin, target, type, args):
        self.insight.append((origin, type, target, args))
    
    CALLBACK_REQUESTNAMES = "RequestNames"
    def register_callback(self, type, callbackfn):
        pass
    
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


class IRCNamesTest(unittest.TestCase):
    
    def test_names_reply(self):
        s = StateDouble()
        c = NamesResponder(s)
        s.channels["#test"].join((1,6), "o")
        s.channels["#test"].join((3,2), "v")
        c.callback_names((3,6), (1, None), ["#test"])
        self.assertEquals(
            [
                ((1,None), "353", (3,6), ["=", "#test", "+test @localtest"]),
                ((1,None), "366", (3,6), ["#test", "End of /NAMES list."])
            ],
            s.insight)
    
    def test_names_reply_if_relevant(self):
        s = StateDouble()
        c = NamesResponder(s)
        c.callback_names((7,6), (2, None), ["#test"])
        self.assertEquals([], s.insight)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
