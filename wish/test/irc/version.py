#!/usr/bin/env python

import unittest

from wish.irc.version import VersionResponder
from wish.irc.state import User, Server, Channel

class StateDouble():
    
    def __init__(self):
        self.insight = []
    
    @property
    def server_id(self):
        return 1
    
    def oobmsg(self, origin, target, type, args):
        self.insight.append((origin, type, target, args))
    
    CALLBACK_REQUESTVERSION = "RequestVersion"
    def register_callback(self, type, callbackfn):
        pass


class IRCVersionTest(unittest.TestCase):
    
    def test_version_reply(self):
        s = StateDouble()
        c = VersionResponder(s)
        c.callback_requestversion((3,6), (1, None))
        self.assertEquals(
            [
                ((1,None), "351", (3,6), ["The WorldIRC Service Host"])
            ],
            s.insight
        )
    
    def test_version_reply_if_relevant(self):
        s = StateDouble()
        c = VersionResponder(s)
        c.callback_requestversion((7,6), (2, None))
        self.assertEquals([], s.insight)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
