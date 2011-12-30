#!/usr/bin/env python

import unittest

from wish.irc.links import LinksResponder
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
        
    CALLBACK_REQUESTLINKS = "RequestLinks"
    
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


class IRCLinksTest(unittest.TestCase):
    
    def test_links_reply(self):
        s = StateDouble()
        c = LinksResponder(s)
        c.callback_links((3,6), (1, None), "*")
        self.assertEquals(
            [
                (
                    (1,None),
                    "364",
                    (3,6),
                    [
                        "test.example.com",
                        "test.example.com",
                        "0 P10 A test description"
                    ]
                ), (
                    (1,None),
                    "365",
                    (3,6),
                    ["*", "End of /LINKS list."]
                )
            ],
            s.insight
        )
    
    def test_links_reply_long(self):
        s = StateDouble()
        c = LinksResponder(s)
        s.servers[1].children = set([2])
        s.servers[2] = Server(1, 2, "test2.example.com", 1234, 1234, 1234,
                              "P10", 0, [], "A test description2")
        s.servers[2].children = set([3])
        s.servers[3] = Server(2, 3, "test3.example.com", 1234, 1234, 1234,
                              "P10", 0, [], "A test description3")
        c.callback_links((3,6), (1, None), "*")
        self.assertEquals(
            [
                (
                    (1,None),
                    "364",
                    (3,6),
                    [
                        "test.example.com",
                        "test.example.com",
                        "0 P10 A test description"
                    ]
                ), (
                    (1,None),
                    "364",
                    (3,6),
                    [
                        "test2.example.com",
                        "test.example.com",
                        "0 P10 A test description2"
                    ]
                ), (
                    (1,None),
                    "364",
                    (3,6),
                    [
                        "test3.example.com",
                        "test2.example.com",
                        "0 P10 A test description3"
                    ]
                ), (
                    (1,None),
                    "365",
                    (3,6),
                    ["*", "End of /LINKS list."]
                )
            ],
            s.insight
        )
    
    def test_links_reply_if_relevant(self):
        s = StateDouble()
        c = LinksResponder(s)
        c.callback_links((7,6), (2, None), "*")
        self.assertEquals([], s.insight)
    
    def test_links_reply_mask(self):
        s = StateDouble()
        c = LinksResponder(s)
        c.callback_links((3,6), (1, None), "*est.example.com")
        self.assertEquals(
            [
                (
                    (1,None),
                    "364",
                    (3,6),
                    [
                        "test.example.com",
                        "test.example.com",
                        "0 P10 A test description"
                    ]
                ), (
                    (1,None),
                    "365",
                    (3,6),
                    ["*est.example.com", "End of /LINKS list."]
                )
            ],
            s.insight
        )
    
    def test_links_reply_if_match(self):
        s = StateDouble()
        c = LinksResponder(s)
        c.callback_links((3,6), (1, None), "foobar.example.com")
        self.assertEquals(
            [
                (
                    (1,None),
                    "365",
                    (3,6),
                    ["foobar.example.com", "End of /LINKS list."]
                )
            ],
            s.insight
        )


def main():
    unittest.main()

if __name__ == '__main__':
    main()
