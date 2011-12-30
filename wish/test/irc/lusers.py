#!/usr/bin/env python

import unittest

from wish.irc.lusers import LusersResponder
from wish.irc.state import User, Channel, Server

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
        self.insight.append((origin, target, type, args))
        
    CALLBACK_REQUESTLUSERS = "RequestLusers"
    def register_callback(self, type, callbackfn):
        pass


class IRCLusersTest(unittest.TestCase):
    
    def test_lusers_reply(self):
        s = StateDouble()
        c = LusersResponder(s)
        c.callback_lusers((3,6), (1, None), "Foo")
        self.assertEquals(
            [
                (
                    (1,None),
                    (3,6),
                    "251",
                    ["There is 1 user on 1 server."]
                ), (
                    (1,None),
                    (3,6),
                    "252",
                    ["0", "operators online."]
                ), (
                    (1,None),
                    (3,6),
                    "254",
                    ["1", "channel formed."]
                ), (
                    (1,None),
                    (3,6),
                    "255",
                    ["I have 1 client and 0 servers."]
                )
            ],
            s.insight
        )
    
    def test_lusers_reply_plural(self):
        s = StateDouble()
        c = LusersResponder(s)
        s.users[(1,2)] = User((1,2), "test2", "test", "example.com",
            [("+o", None)], 6, 0, 1234, "Joe Bloggs")
        s.servers[1].children = set([2])
        s.servers[2] = Server(1, 2, "test2.example.com", 1234, 1234, 1234,
                              "P10", 0, [], "A test description")
        s.channels["#test2"] = Channel("#test2", 1234)
        c.callback_lusers((3,6), (1, None), "Foo")
        self.assertEquals(
            [
                (
                    (1,None),
                    (3,6),
                    "251",
                    ["There are 2 users on 2 servers."]
                ), (
                    (1,None),
                    (3,6),
                    "252",
                    ["1", "operator online."]
                ), (
                    (1,None),
                    (3,6),
                    "254",
                    ["2", "channels formed."]
                ), (
                    (1,None),
                    (3,6),
                    "255",
                    ["I have 2 clients and 1 server."]
                )
            ],
            s.insight)
    
    def test_lusers_reply_if_relevant(self):
        s = StateDouble()
        c = LusersResponder(s)
        c.callback_lusers((7,6), (2, None), "Foo")
        self.assertEquals([], s.insight)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
