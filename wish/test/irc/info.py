#!/usr/bin/env python

import unittest

from wish.irc.info import InfoResponder
from wish.irc.state import User, Server, Channel

class StateDouble():
    
    def __init__(self):
        self.insight = []
        self.max_client_numerics = {1: 262143}
        self.users = {
            (1,1): User((1,1), "test", "test", "example.com", [], 6,
                        0, 1234, "Joe Bloggs")
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
        
    CALLBACK_REQUESTINFO = "RequestInfo"
    
    def register_callback(self, type, callbackfn):
        pass


class IRCInfoTest(unittest.TestCase):
    
    def test_info_reply(self):
        s = StateDouble()
        c = InfoResponder(s)
        c.callback_inforequest((3,6), (1, None))
        self.assertEquals(
            [
                (
                    (1,None),
                    (3,6),
                    "371",
                    ["I know 1 server and 1 user on 1 channel."]
                ), (
                    (1,None),
                    (3,6),
                    "374",
                    ["End of /INFO list"]
                )
            ],
            s.insight
        )
    
    def test_info_reply_plural(self):
        s = StateDouble()
        c = InfoResponder(s)
        s.users[(1,2)] = User(
            (1,2), "test2", "test", "example.com", [("+o", None)], 6, 0,
            1234, "Joe Bloggs")
        s.servers[1].children = set([2])
        s.servers[2] = Server(1, 2, "test2.example.com", 1234, 1234, 1234,
                              "P10", 0, [], "A test description")
        s.channels["#test2"] = Channel("#test2", 1234)
        c.callback_inforequest((3,6), (1, None))
        self.assertEquals(
            [
                (
                    (1,None),
                    (3,6),
                    "371",
                    ["I know 2 servers and 2 users on 2 channels."]
                ), (
                    (1,None),
                    (3,6),
                    "374",
                    ["End of /INFO list"]
                )
            ],
            s.insight
        )
    
    def test_info_reply_if_relevant(self):
        s = StateDouble()
        c = InfoResponder(s)
        c.callback_inforequest((7,6), (2, None))
        self.assertEquals([], s.insight)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
