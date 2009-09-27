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
    def __init__(self):
        self.maxClientNumerics = dict({1: 262143})
        self.users = dict({(1,1): irc.state.user((1,1), "test", "test", "example.com", [], 6, 0, 1234, "Joe Bloggs")})
        self.servers = dict({1: irc.state.server(None, 1, "test.example.com", 1234, 1234, 1234, "P10", 0, [], "A test description")})
        self.channels = dict({"#test": irc.state.channel("#test", 1234)})
    def glines(self):
        return [("*!test@example.com", "A test description", 3600, True, 1000), ("*!test8@example.com", "Another test description", 3634, True, 1234)]
    def jupes(self):
        return [("test.example.com", "A test description", 3600, True, 1000), ("test2.example.com", "Another test description", 3634, True, 1234)]
    def getServerID(self):
        return 1
    def getServerName(self):
        return "test.example.com"
    def getAdminName(self):
        return "tester"
    def getContactEmail(self):
        return "test@example.com"
    def getServerDescription(self):
        return "A testing server in Test, USA"
    def getNextHop(self, dest):
        if dest[0] == 1:
            return None
        elif dest[0] == 2 or dest[0] == 3:
            return 2
        else:
            return 6
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
    def nick2numeric(self, nick):
        if nick == "test2.example.com":
            return (2, None)
        elif nick == "test9.example.com":
            return (9, None)
    def ts(self):
        return 1000

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
    
    def testChannelChangeMode(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackChannelChangeMode(((1, 6), "#test", [("+c", None)]))
        self.assertEquals([((1, 6), "M", ["#test", "+c", "1234"])], c.insight)
    
    def testChannelChangeModeIntArg(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackChannelChangeMode(((1, 6), "#test", [("+l", 7)]))
        self.assertEquals([((1, 6), "M", ["#test", "+l", "7", "1234"])], c.insight)
    
    def testChannelChangeModeStringArg(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackChannelChangeMode(((1, 6), "#test", [("+k", "string")]))
        self.assertEquals([((1, 6), "M", ["#test", "+k", "string", "1234"])], c.insight)
    
    def testChannelChangeMultiModeStringArg(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackChannelChangeMode(((1, 6), "#test", [("+C", None), ("+k", "string")]))
        self.assertEquals([((1, 6), "M", ["#test", "+Ck", "string", "1234"])], c.insight)
    
    def testChannelChangeModeIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackChannelChangeMode(((2, 6), "#test", [("+c", None)]))
        self.assertEquals([], c.insight)
    
    def testChannelAddBan(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackChannelAddBan(((1, 6), "#test", "*!*@test.example.com"))
        self.assertEquals([((1, 6), "M", ["#test", "+b", "*!*@test.example.com", "1234"])], c.insight)
    
    def testChannelAddBanIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackChannelAddBan(((3, 6), "#test", "*!*@test.example.com"))
        self.assertEquals([], c.insight)
    
    def testChannelRemoveBan(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackChannelRemoveBan(((1, 6), "#test", "*!*@test.example.com"))
        self.assertEquals([((1, 6), "M", ["#test", "-b", "*!*@test.example.com", "1234"])], c.insight)
    
    def testChannelRemoveBanIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackChannelRemoveBan(((3, 6), "#test", "*!*@test.example.com"))
        self.assertEquals([], c.insight)
    
    def testChannelClearBans(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackChannelClearBans(((1, 6), "#test"))
        self.assertEquals([((1,6), "CM", ["#test", "b"])], c.insight)
    
    def testChannelClearBansIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackChannelClearBans(((2, 6), "#test"))
        self.assertEquals([], c.insight)
    
    def testChannelChannelOp(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackChannelOp(((1, 6), "#test", (2, 3)))
        self.assertEquals([((1, 6), "M", ["#test", "+o", "ACAAD", "1234"])], c.insight)
    
    def testChannelChannelOpIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackChannelOp(((3, 6), "#test", (2, 3)))
        self.assertEquals([], c.insight)
    
    def testChannelChannelDeop(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackChannelDeop(((1, 6), "#test", (2,3)))
        self.assertEquals([((1, 6), "M", ["#test", "-o", "ACAAD", "1234"])], c.insight)
    
    def testChannelChannelDeopIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackChannelDeop(((2, 6), "#test", (2,3)))
        self.assertEquals([], c.insight)
    
    def testChannelClearOps(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackChannelClearOps(((1, 6), "#test"))
        self.assertEquals([((1,6), "CM", ["#test", "o"])], c.insight)
    
    def testChannelClearOpsIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackChannelClearOps(((2, 6), "#test"))
        self.assertEquals([], c.insight)
    
    def testChannelChannelVoice(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackChannelVoice(((1, 6), "#test", (2, 3)))
        self.assertEquals([((1, 6), "M", ["#test", "+v", "ACAAD", "1234"])], c.insight)
    
    def testChannelChannelVoiceIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackChannelVoice(((3, 6), "#test", (2, 3)))
        self.assertEquals([], c.insight)
    
    def testChannelChannelDevoice(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackChannelDevoice(((1, 6), "#test", (2,3)))
        self.assertEquals([((1, 6), "M", ["#test", "-v", "ACAAD", "1234"])], c.insight)
    
    def testChannelChannelDevoiceIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackChannelDevoice(((2, 6), "#test", (2,3)))
        self.assertEquals([], c.insight)
    
    def testChannelClearVoices(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackChannelClearVoices(((1, 6), "#test"))
        self.assertEquals([((1,6), "CM", ["#test", "v"])], c.insight)
    
    def testChannelClearVoicesIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackChannelClearVoices(((2, 6), "#test"))
        self.assertEquals([], c.insight)
    
    def testGlineAdd(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackGlineAdd(((1, None), "*!test@example.com", None, 3600, "A test description"))
        self.assertEquals([((1, None), "GL", ["*", "+*!test@example.com", "2600", "1000", "A test description"])], c.insight)
    
    def testGlineAddIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackGlineAdd(((2, None), "*!test@example.com", None, 2400, "A test description"))
        self.assertEquals([], c.insight)
    
    def testGlineAddTarget(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackGlineAdd(((1, None), "*!test@example.com", 3, 3600, "A test description"))
        self.assertEquals([((1, None), "GL", ["AD", "+*!test@example.com", "2600", "1000", "A test description"])], c.insight)
    
    def testGlineAddTargetIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackGlineAdd(((1, None), "*!test@example.com", 9, 2400, "A test description"))
        self.assertEquals([], c.insight)
    
    def testGlineRemove(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackGlineRemove(((1, None), "*!test@example.com", None))
        self.assertEquals([((1, None), "GL", ["*", "-*!test@example.com", "2600", "1000", "A test description"])], c.insight)
    
    def testGlineRemoveIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackGlineRemove(((3, None), "*!test@example.com", None))
        self.assertEquals([], c.insight)
    
    def testGlineRemoveTarget(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackGlineRemove(((1, None), "*!test@example.com", 2))
        self.assertEquals([((1, None), "GL", ["AC", "-*!test@example.com", "2600", "1000", "A test description"])], c.insight)
    
    def testGlineRemoveTargetIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackGlineRemove(((1, None), "*!test@example.com", 8))
        self.assertEquals([], c.insight)
    
    def testInvite(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackInvite(((1, 6), (3, 2), "#test"))
        self.assertEquals([((1,6), "I", ["test", "#test"])], c.insight)
    
    def testInviteIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackInvite(((1, 6), (7, 1), "#test"))
        self.assertEquals([], c.insight)
    
    def testJupeAdd(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackJupeAdd(((1, None), "test.example.com", None, 3600, "A test description"))
        self.assertEquals([((1, None), "JU", ["*", "+test.example.com", "2600", "1000", "A test description"])], c.insight)
    
    def testJupeAddIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackJupeAdd(((2, None), "test.example.com", None, 2400, "A test description"))
        self.assertEquals([], c.insight)
    
    def testJupeAddTarget(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackJupeAdd(((1, None), "test.example.com", 3, 3600, "A test description"))
        self.assertEquals([((1, None), "JU", ["AD", "+test.example.com", "2600", "1000", "A test description"])], c.insight)
    
    def testJupeAddTargetIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackJupeAdd(((1, None), "test.example.com", 9, 2400, "A test description"))
        self.assertEquals([], c.insight)
    
    def testJupeRemove(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackJupeRemove(((1, None), "test.example.com", None))
        self.assertEquals([((1, None), "JU", ["*", "-test.example.com", "2600", "1000", "A test description"])], c.insight)
    
    def testJupeRemoveIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackJupeRemove(((3, None), "test.example.com", None))
        self.assertEquals([], c.insight)
    
    def testJupeRemoveTarget(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackJupeRemove(((1, None), "test.example.com", 2))
        self.assertEquals([((1, None), "JU", ["AC", "-test.example.com", "2600", "1000", "A test description"])], c.insight)
    
    def testJupeRemoveTargetIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackJupeRemove(((1, None), "test.example.com", 8))
        self.assertEquals([], c.insight)
    
    def testAdminSend(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackAdminInfo(((1,6), (3, None)))
        self.assertEquals([((1,6), "AD", ["AD"])], c.insight)
    
    def testAdminSendIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackAdminInfo(((1,6), (7, None)))
        self.assertEquals([], c.insight)
    
    def testInfoSend(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackInfoRequest(((1,6), (3, None)))
        self.assertEquals([((1,6), "F", ["AD"])], c.insight)
    
    def testInfoSendIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackInfoRequest(((1,6), (7, None)))
        self.assertEquals([], c.insight)
    
    def testKick(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackKick(((1, 6), "#test", (5,2), "A reason"))
        self.assertEquals([((1,6), "K", ["#test", "AFAAC", "A reason"])], c.insight)
    
    def testKickIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackKick(((3, 6), "#test", (5,2), "A reason"))
        self.assertEquals([], c.insight)
    
    def testZombiePart(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackZombiePart(((1, 6), "#test"))
        self.assertEquals([((1,6), "P", ["#test", "Zombie parting channel"])], c.insight)
    
    def testZombiePartIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackZombiePart(((3, 6), "#test"))
        self.assertEquals([], c.insight)
    
    def testDestruct(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackChannelDestroy(((1, 6), "#test", 1234))
        self.assertEquals([((1,6), "DE", ["#test", "1234"])], c.insight)
    
    def testDestructIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackChannelDestroy(((3, 6), "#test", 1234))
        self.assertEquals([], c.insight)
    
    def testQuit(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackQuit(((1, 6), "Quitting network", False))
        self.assertEquals([((1,6), "Q", ["Quitting network"])], c.insight)
    
    def testQuitIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackQuit(((3, 6), "Quitting network", False))
        self.assertEquals([], c.insight)
    
    def testQuitOnlyPropagatedIfNotSquit(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackQuit(((1, 6), "Quitting network", True))
        self.assertEquals([], c.insight)
    
    def testKill(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackKill(((1, 6), (3,6), ["test.example.com", "origin.example.com"], "Being naughty"))
        self.assertEquals([((1,6), "D", ["ADAAG", "test.example.com!origin.example.com (Being naughty)"])], c.insight)
    
    def testKillIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackKill(((1, 6), (5,6), "test.example.com", "Being naughty"))
        self.assertEquals([], c.insight)
    
    def testLusersSend(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackLusers(((1,6), (3, None), "Foo"))
        self.assertEquals([((1,6), "LU", ["Foo", "AD"])], c.insight)
    
    def testLusersSendIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackLusers(((1,6), (7, None), "Foo"))
        self.assertEquals([], c.insight)
    
    def testLinksSend(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackLinks(((1,6), (3, None), "*"))
        self.assertEquals([((1,6), "LI", ["AD", "*"])], c.insight)
    
    def testLinksSendIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackLinks(((1,6), (7, None), "*"))
        self.assertEquals([], c.insight)
    
    def testUserChangeMode(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackChangeUserMode(((1, 6), [("+c", None)]))
        self.assertEquals([((1, 6), "M", ["localtest", "+c"])], c.insight)
    
    def testUserChangeModeIntArg(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackChangeUserMode(((1, 6), [("+l", 7)]))
        self.assertEquals([((1, 6), "M", ["localtest", "+l", "7"])], c.insight)
    
    def testUserChangeModeStringArg(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackChangeUserMode(((1, 6), [("+k", "string")]))
        self.assertEquals([((1, 6), "M", ["localtest", "+k", "string"])], c.insight)
    
    def testUserChangeMultiModeStringArg(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackChangeUserMode(((1, 6), [("+C", None), ("+k", "string")]))
        self.assertEquals([((1, 6), "M", ["localtest", "+Ck", "string"])], c.insight)
    
    def testUserChangeModeIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackChangeUserMode(((2, 6), [("+c", None)]))
        self.assertEquals([], c.insight)
    
    def testMOTDSend(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackMOTD(((1,6), (3, None)))
        self.assertEquals([((1,6), "MO", ["AD"])], c.insight)
    
    def testMOTDSendIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackMOTD(((1,6), (7, None)))
        self.assertEquals([], c.insight)
    
    def testNamesSend(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackNames(((1,6), (3, None), ["#test"]))
        self.assertEquals([((1,6), "E", ["#test", "AD"])], c.insight)
    
    def testNamesSendIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackNames(((1,6), (7, None), ["#test"]))
        self.assertEquals([], c.insight)
    
    def testTopic(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackTopic(((1,6), "#test", "New topic", 1234, 12345))
        self.assertEquals([((1,6), "T", ["#test", "12345", "1234", "New topic"])], c.insight)
    
    def testTopicIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackTopic(((2,6), "#test", "New topic", 1234, 1234))
        self.assertEquals([], c.insight)
    
    def testSilenceAdd(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackSilenceAdd(((1,6), "*@example.com"))
        self.assertEquals([((1,6), "U", ["*", "*@example.com"])], c.insight)
    
    def testSilenceAddIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackSilenceAdd(((2,6), "*@example.com"))
        self.assertEquals([], c.insight)
    
    def testSilenceAdd(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackSilenceRemove(((1,6), "*@example.com"))
        self.assertEquals([((1,6), "U", ["*", "-*@example.com"])], c.insight)
    
    def testSilenceAddIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackSilenceRemove(((2,6), "*@example.com"))
        self.assertEquals([], c.insight)
    
    def testVersionSend(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackRequestVersion(((1,6), (3, None)))
        self.assertEquals([((1,6), "V", ["AD"])], c.insight)
    
    def testVersionSendIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackRequestVersion(((1,6), (7, None)))
        self.assertEquals([], c.insight)
    
    def testOobmsg(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackOobmsg(((1, None), (3,6), "123", ["Arg1", "Arg 2"]))
        self.assertEquals([((1, None), "123", ["ADAAG", "Arg1", "Arg 2"])], c.insight)
    
    def testOobmsgIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackOobmsg(((1, None), (6,6), "123", ["Arg1", "Arg 2"]))
        self.assertEquals([], c.insight)
    
    def testPingSend(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackPing(((1, None), "test", (3, None)))
        self.assertEquals([((1,None), "G", ["test", "AD"])], c.insight)
    
    def testPingSendIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackPing(((1, None), "test", (7, None)))
        self.assertEquals([], c.insight)
    
    def testPingReply(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackPing(((3, None), "test", (1, None)))
        self.assertEquals([((1,None), "Z", ["AB", "test"])], c.insight)
    
    def testPingReplyIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackPing(((7, None), "test", (1, None)))
        self.assertEquals([], c.insight)
    
    def testPongSend(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackPong(((1, None), (1, None), (3, None)))
        self.assertEquals([((1,None), "Z", ["AB", "AD"])], c.insight)
    
    def testPongSendIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackPong(((1, None), "test", (7, None)))
        self.assertEquals([], c.insight)
    
    def testWallusers(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackWallusers(((6,2), "A message"))
        self.assertEquals([((6,2), "WU", ["A message"])], c.insight)
    
    def testWallusersIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackWallusers(((3,2), "A message"))
        self.assertEquals([], c.insight)
    
    def testWallops(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackWallops(((6,2), "A message"))
        self.assertEquals([((6,2), "WA", ["A message"])], c.insight)
    
    def testWallopsIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackWallops(((3,2), "A message"))
        self.assertEquals([], c.insight)
    
    def testWallvoices(self):
        s = StateDouble()
        c = TestableConnection(s)
        s.channels["#test"].join((3,2), "v")
        c.callbackWallvoices(((1, 6), "#test", "A message"))
        self.assertEquals([((1,6), "WV", ["#test", "A message"])], c.insight)
    
    def testWallvoicesIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        s.channels["#test"].join((3,2), "v")
        c.callbackWallvoices(((3, 6), "#test", "A message"))
        self.assertEquals([], c.insight)
    
    def testWallvoicesIfSpecific(self):
        s = StateDouble()
        c = TestableConnection(s)
        s.channels["#test"].join((3,2), "")
        c.callbackWallvoices(((1, 6), "#test", "A message"))
        self.assertEquals([], c.insight)
    
    def testWallvoicesIfOp(self):
        s = StateDouble()
        c = TestableConnection(s)
        s.channels["#test"].join((3,2), "o")
        c.callbackWallvoices(((1, 6), "#test", "A message"))
        self.assertEquals([((1,6), "WV", ["#test", "A message"])], c.insight)
    
    def testWallvoicesOnlyOnce(self):
        s = StateDouble()
        c = TestableConnection(s)
        s.channels["#test"].join((3,2), "v")
        s.channels["#test"].join((3,9), "o")
        c.callbackWallvoices(((1, 6), "#test", "A message"))
        self.assertEquals([((1,6), "WV", ["#test", "A message"])], c.insight)
    
    def testWallchops(self):
        s = StateDouble()
        c = TestableConnection(s)
        s.channels["#test"].join((3,2), "o")
        c.callbackWallchops(((1, 6), "#test", "A message"))
        self.assertEquals([((1,6), "WC", ["#test", "A message"])], c.insight)
    
    def testWallchopsIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        s.channels["#test"].join((3,2), "o")
        c.callbackWallchops(((3, 6), "#test", "A message"))
        self.assertEquals([], c.insight)
    
    def testWallchopsIfSpecific(self):
        s = StateDouble()
        c = TestableConnection(s)
        s.channels["#test"].join((3,2), "")
        c.callbackWallchops(((1, 6), "#test", "A message"))
        self.assertEquals([], c.insight)
    
    def testWallchopsExcludesVoice(self):
        s = StateDouble()
        c = TestableConnection(s)
        s.channels["#test"].join((3,2), "v")
        c.callbackWallchops(((1, 6), "#test", "A message"))
        self.assertEquals([], c.insight)
    
    def testWallchopsOnlyOnce(self):
        s = StateDouble()
        c = TestableConnection(s)
        s.channels["#test"].join((3,2), "o")
        s.channels["#test"].join((3,9), "o")
        c.callbackWallchops(((1, 6), "#test", "A message"))
        self.assertEquals([((1,6), "WC", ["#test", "A message"])], c.insight)
    
    def testWhoisSend(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackRequestWhois(((1,6), (3, None), "test"))
        self.assertEquals([((1,6), "W", ["AD", "test"])], c.insight)
    
    def testWhoisSendIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackRequestWhois(((1,6), (7, None), "test"))
        self.assertEquals([], c.insight)
    
    def testTraceSend(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackTrace(((1,6), "test", (3, None)))
        self.assertEquals([((1,6), "TR", ["test", "AD"])], c.insight)
    
    def testTraceSendIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackTrace(((1,6), "test", (7, None)))
        self.assertEquals([], c.insight)
    
    def testStatsSend(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackRequestStats(((1,6), (3, None), "B", "Search"))
        self.assertEquals([((1,6), "R", ["B", "AD", "Search"])], c.insight)
    
    def testStatsSendNoExtra(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackRequestStats(((1,6), (3, None), "B", None))
        self.assertEquals([((1,6), "R", ["B", "AD"])], c.insight)
    
    def testStatsSendIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackRequestStats(((1,6), (7, None), "B", None))
        self.assertEquals([], c.insight)
    
    def testPrivmsgPerson(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackPrivmsg(((1, 6), (3,1), "A message"))
        self.assertEquals([((1,6), "P", ["ADAAB", "A message"])], c.insight)
    
    def testPrivmsgPersonIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackPrivmsg(((1, 6), (9,1), "A message"))
        self.assertEquals([], c.insight)
    
    def testPrivmsgLong(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackPrivmsg(((1, 6), "test@test2.example.com", "A message"))
        self.assertEquals([((1,6), "P", ["test@test2.example.com", "A message"])], c.insight)
    
    def testPrivmsgLongIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackPrivmsg(((1, 6), "test@test9.example.com", "A message"))
        self.assertEquals([], c.insight)
    
    def testPrivmsgChannel(self):
        s = StateDouble()
        c = TestableConnection(s)
        s.channels["#test"].join((3,2), "")
        c.callbackPrivmsg(((1, 6), "#test", "A message"))
        self.assertEquals([((1,6), "P", ["#test", "A message"])], c.insight)
    
    def testPrivmsgChannelIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        s.channels["#test"].join((3,2), "")
        c.callbackPrivmsg(((3, 6), "#test", "A message"))
        self.assertEquals([], c.insight)
    
    def testPrivmsgChannelIfSpecific(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackPrivmsg(((1, 6), "#test", "A message"))
        self.assertEquals([], c.insight)
    
    def testPrivmsgServer(self):
        s = StateDouble()
        c = TestableConnection(s)
        s.servers[2] = irc.state.server(1, 2, "test2.example.com", 1234, 1234, 1234, "P10", 0, [], "A test description")
        c.callbackPrivmsg(((1,6), "$test2.example.com", "A message"))
        self.assertEquals([((1,6), "P", ["$test2.example.com", "A message"])], c.insight)
    
    def testPrivmsgServerIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        s.servers[9] = irc.state.server(1, 9, "test9.example.com", 1234, 1234, 1234, "P10", 0, [], "A test description")
        c.callbackPrivmsg(((1,6), "$test9.example.com", "A message"))
        self.assertEquals([], c.insight)
    
    def testPrivmsgServerMask(self):
        s = StateDouble()
        c = TestableConnection(s)
        s.servers[2] = irc.state.server(1, 2, "test2.example.com", 1234, 1234, 1234, "P10", 0, [], "A test description")
        c.callbackPrivmsg(((1,6), "$test*.example.com", "A message"))
        self.assertEquals([((1,6), "P", ["$test*.example.com", "A message"])], c.insight)
    
    def testNoticePerson(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackNotice(((1, 6), (3,1), "A message"))
        self.assertEquals([((1,6), "O", ["ADAAB", "A message"])], c.insight)
    
    def testNoticePersonIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackNotice(((1, 6), (9,1), "A message"))
        self.assertEquals([], c.insight)
    
    def testNoticeLong(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackNotice(((1, 6), "test@test2.example.com", "A message"))
        self.assertEquals([((1,6), "O", ["test@test2.example.com", "A message"])], c.insight)
    
    def testNoticeLongIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackNotice(((1, 6), "test@test9.example.com", "A message"))
        self.assertEquals([], c.insight)
    
    def testNoticeChannel(self):
        s = StateDouble()
        c = TestableConnection(s)
        s.channels["#test"].join((3,2), "")
        c.callbackNotice(((1, 6), "#test", "A message"))
        self.assertEquals([((1,6), "O", ["#test", "A message"])], c.insight)
    
    def testNoticeChannelIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        s.channels["#test"].join((3,2), "")
        c.callbackNotice(((3, 6), "#test", "A message"))
        self.assertEquals([], c.insight)
    
    def testNoticeChannelIfSpecific(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackNotice(((1, 6), "#test", "A message"))
        self.assertEquals([], c.insight)
    
    def testNoticeServer(self):
        s = StateDouble()
        c = TestableConnection(s)
        s.servers[2] = irc.state.server(1, 2, "test2.example.com", 1234, 1234, 1234, "P10", 0, [], "A test description")
        c.callbackNotice(((1,6), "$test2.example.com", "A message"))
        self.assertEquals([((1,6), "O", ["$test2.example.com", "A message"])], c.insight)
    
    def testNoticeServerIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        s.servers[9] = irc.state.server(1, 9, "test9.example.com", 1234, 1234, 1234, "P10", 0, [], "A test description")
        c.callbackNotice(((1,6), "$test9.example.com", "A message"))
        self.assertEquals([], c.insight)
    
    def testNoticeServerMask(self):
        s = StateDouble()
        c = TestableConnection(s)
        s.servers[2] = irc.state.server(1, 2, "test2.example.com", 1234, 1234, 1234, "P10", 0, [], "A test description")
        c.callbackNotice(((1,6), "$test*.example.com", "A message"))
        self.assertEquals([((1,6), "O", ["$test*.example.com", "A message"])], c.insight)


def main():
    unittest.main()

if __name__ == '__main__':
    main()