#!/usr/bin/env python

import unittest
import irc.lusers

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
        self.insight.append((origin, target, type, args))
    CALLBACK_REQUESTLUSERS = "RequestLusers"
    def registerCallback(self, type, callbackfn):
        pass
    def getServerID(self):
        return 1

class IRCLusersTest(unittest.TestCase):
    
    def testLusersReply(self):
        s = StateDouble()
        c = irc.lusers.lusers(s)
        c.callbackLusers(((3,6), (1, None), "Foo"))
        self.assertEquals([((1,None), (3,6), "251", ["There is 1 user on 1 server."]), ((1,None), (3,6), "252", ["0", "operators online."]), ((1,None), (3,6), "254", ["1", "channel formed."]), ((1,None), (3,6), "255", ["I have 1 client and 0 servers."])], s.insight)
    
    def testLusersReplyPlural(self):
        s = StateDouble()
        c = irc.lusers.lusers(s)
        s.users[(1,2)] = irc.state.user((1,2), "test2", "test", "example.com", [("+o", None)], 6, 0, 1234, "Joe Bloggs")
        s.servers[1].children = set([2])
        s.servers[2] = irc.state.server(1, 2, "test2.example.com", 1234, 1234, 1234, "P10", 0, [], "A test description")
        s.channels["#test2"] = irc.state.channel("#test2", 1234)
        c.callbackLusers(((3,6), (1, None), "Foo"))
        self.assertEquals([((1,None), (3,6), "251", ["There are 2 users on 2 servers."]), ((1,None), (3,6), "252", ["1", "operator online."]), ((1,None), (3,6), "254", ["2", "channels formed."]), ((1,None), (3,6), "255", ["I have 2 clients and 1 server."])], s.insight)
    
    def testLusersReplyIfRelevant(self):
        s = StateDouble()
        c = irc.lusers.lusers(s)
        c.callbackLusers(((7,6), (2, None), "Foo"))
        self.assertEquals([], s.insight)

def main():
    unittest.main()

if __name__ == '__main__':
    main()