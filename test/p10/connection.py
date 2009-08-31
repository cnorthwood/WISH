#!/usr/bin/env python

import unittest
import p10.connection
import irc.state

class TestableConnection(p10.connection.connection):
    insight = []
    def __init__(self, state):
        self.insight = []
        p10.connection.connection.__init__(self, state)
        self.numeric = 2
    def _sendLine(self, origin, command, args):
        self.insight.append((origin, command, args))
    def registerCallback(self, callback, fn):
        pass
    def close_connection(self):
        self.connstate = self.COMPLETE

class StateDouble:
    maxClientNumerics = dict({1: 262143})
    channels = dict({"#test": irc.state.channel("#test", 1234)})
    def getServerID(self):
        return 1
    def getServerName(self):
        return "test.example.com"
    def getNextHop(self, dest):
        if dest[0] == 1:
            return None
        elif dest[0] == 2 or dest[0] == 3:
            return 2
        else:
            return 6
    def numeric2nick(self, numeric):
        if numeric == (3, None):
            return "test3.example.com"

class ConnectionTest(unittest.TestCase):
    
    def testCanInit(self):
        s = StateDouble()
        c = TestableConnection(s)
    
    def testIntroduceServer(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackNewServer(((1, None), 8, "test.example.com", 262143, 1234, 1234, "P10", 1, "", "A testing server"))
        self.assertEquals([((1, None), "S", ["test.example.com", "2", "1234", "1234", "P10", "AI]]]", "+", "A testing server"])], c.insight)
    
    def testIntroduceServerOnlyAppropriate(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackNewServer(((2, None), 3, "test.example.com", 262143, 1234, 1234, "P10", 1, "", "A testing server"))
        c.callbackNewServer(((3, None), 12, "test2.example.com", 262143, 1234, 1234, "P10", 1, "", "A testing server"))
        self.assertEquals([], c.insight)
    
    def testIntroduceUser(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackNewUser(((1, None), (1,2), "test", "test", "example.com", [], 1, 1, 1234, "A test user"))
        self.assertEquals([((1, None), "N", ["test", "2", "1234", "test", "example.com", "AAAAAB", "ABAAC", "A test user"])], c.insight)
    
    def testIntroduceUserWithModes(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackNewUser(((1, None), (1,2), "test", "test", "example.com", [("+x", None)], 1, 1, 1234, "A test user"))
        self.assertEquals([((1, None), "N", ["test", "2", "1234", "test", "example.com", "+x", "AAAAAB", "ABAAC", "A test user"])], c.insight)
    
    def testIntroduceUserWithModesAndArg(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackNewUser(((1, None), (1,2), "test", "test", "example.com", [("+r", "Test")], 1, 1, 1234, "A test user"))
        self.assertEquals([((1, None), "N", ["test", "2", "1234", "test", "example.com", "+r", "Test", "AAAAAB", "ABAAC", "A test user"])], c.insight)
    
    def testIntroduceUserOnlyIfAppropriate(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackNewUser(((2, None), (2,2), "test", "test", "example.com", [("+r", "Test")], 1, 1, 1234, "A test user"))
        self.assertEquals([], c.insight)
    
    def testChangeNick(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackChangeNick(((1, 6), (1,6), "test2", 68))
        self.assertEquals([((1,6), "N", ["test2", "68"])], c.insight)
    
    def testChangeNickSvs(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackChangeNick(((1, None), (1,6), "test2", 68))
        self.assertEquals([((1,None), "SN", ["ABAAG", "test2"])], c.insight)
    
    def testChangeNickIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackChangeNick(((2, 6), (2,6), "test2", 68))
        self.assertEquals([], c.insight)
    
    def testSquit(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackSquit(((4, None), (3, None), "Test Quit", 68))
        self.assertEquals([((4, None), "SQ", ["test3.example.com", "68", "Test Quit"])], c.insight)
    
    def testSquitIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackSquit(((2, None), (6, None), "Test Quit", 68))
        self.assertEquals([], c.insight)

    def testSquitMe(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackSquit(((1, None), (2, None), "Test Quit", 68))
        self.assertEquals([((1, None), "SQ", ["test.example.com", "0", "Test Quit"])], c.insight)
        self.assertEquals(c.COMPLETE, c.connstate)
    
    def testAuthenticate(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackAuthenticate(((6, None), (1, 3), "example"))
        self.assertEquals([((6, None), "AC", ["ABAAD", "example"])], c.insight)
    
    def testAuthenticateIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackAuthenticate(((2, None), (1, 3), "example"))
        self.assertEquals([], c.insight)
    
    def testAway(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackAway(((6, 3), "example"))
        self.assertEquals([((6, 3), "A", ["example"])], c.insight)
    
    def testAwayIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackAway(((3, 3), "example"))
        self.assertEquals([], c.insight)
    
    def testBack(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackBack(((6, 3)))
        self.assertEquals([((6, 3), "A", [])], c.insight)
    
    def testBackIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackBack(((3, 3)))
        self.assertEquals([], c.insight)
    
    def testCreate(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackChannelCreate(((1, None), "#test", 1234))
        self.assertEquals([((1, None), "C", ["#test", "1234"])], c.insight)
    
    def testCreateIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackChannelCreate(((3, None), "#test", 1234))
        self.assertEquals([], c.insight)
    
    def testJoin(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackChannelJoin(((1, 6), (1, 6), "#test", "", 1234))
        self.assertEquals([((1, 6), "J", ["#test", "1234"])], c.insight)
    
    def testJoinIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackChannelJoin(((3, 6), (3, 6), "#test", "", 1234))
        self.assertEquals([], c.insight)
    
    def testJoinSendModes(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackChannelJoin(((1, 6), (1, 6), "#test", "ov", 1234))
        self.assertEquals([((1, 6), "J", ["#test", "1234"]), ((1,6), "M", ["#test", "+o", "ABAAG", "1234"]), ((1,6), "M", ["#test", "+v", "ABAAG", "1234"])], c.insight)
    
    def testSvsjoin(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackChannelJoin(((1, None), (1, 6), "#test", "", 1234))
        self.assertEquals([((1, None), "SJ", ["ABAAG", "#test"])], c.insight)
    
    def testPart(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackChannelPart(((1, 6), "#test", "Reason"))
        self.assertEquals([((1,6), "P", ["#test", "Reason"])], c.insight)
    
    def testPartIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackChannelPart(((3, 6), "#test", "Reason"))
        self.assertEquals([], c.insight)
    
    def testPartAll(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackPartAll(((1, 6)))
        self.assertEquals([((1,6), "J", ["0"])], c.insight)
    
    def testPartAllIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackPartAll(((3, 6)))
        self.assertEquals([], c.insight)

def main():
    unittest.main()

if __name__ == '__main__':
    main()