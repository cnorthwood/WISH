#!/usr/bin/env python

import unittest
import irc.info

class StateDouble:
    insight = []
    users = dict()
    servers = dict()
    channels = dict()
    def __init__(self):
        self.insight = []
        self.maxClientNumerics = dict({1: 262143})
        self.users = dict({(1,1): irc.state.user((1,1), "test", "test", "example.com", [], 6, 0, 1234, "Joe Bloggs")})
        self.servers = dict({1: irc.state.server(None, 1, "test.example.com", 1234, 1234, 1234, "P10", 0, [], "A test description")})
        self.channels = dict({"#test": irc.state.channel("#test", 1234)})
    def getServerID(self):
        return 1
    def oobmsg(self, origin, target, type, args):
        self.insight.append((origin, type, target, args))
    CALLBACK_REQUESTINFO = "RequestInfo"
    def registerCallback(self, type, callbackfn):
        pass
    def getServerID(self):
        return 1

class IRCInfoTest(unittest.TestCase):
    
    def testInfoReply(self):
        s = StateDouble()
        c = irc.info.info(s)
        c.callbackInfoRequest(((3,6), (1, None)))
        self.assertEquals([((1,None), (3,6), "371", ["I know 1 server and 1 user on 1 channel."]), ((1,None), (3,6), "374", ["End of /INFO list"])], s.insight)
    
    def testInfoReplyPlural(self):
        s = StateDouble()
        c = irc.info.info(s)
        s.users[(1,2)] = irc.state.user((1,2), "test2", "test", "example.com", [("+o", None)], 6, 0, 1234, "Joe Bloggs")
        s.servers[1].children = set([2])
        s.servers[2] = irc.state.server(1, 2, "test2.example.com", 1234, 1234, 1234, "P10", 0, [], "A test description")
        s.channels["#test2"] = irc.state.channel("#test2", 1234)
        c.callbackInfoRequest(((3,6), (1, None)))
        self.assertEquals([((1,None), (3,6), "371", ["I know 2 servers and 2 users on 2 channels."]), ((1,None), (3,6), "374", ["End of /INFO list"])], s.insight)
    
    def testInfoReplyIfRelevant(self):
        s = StateDouble()
        c = irc.info.info(s)
        c.callbackInfoRequest(((7,6), (2, None)))
        self.assertEquals([], s.insight)

def main():
    unittest.main()

if __name__ == '__main__':
    main()