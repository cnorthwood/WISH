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
    
    def testAdminReply(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackAdminInfo(((3,6), (1, None)))
        self.assertEquals([((1,None), "256", ["ADAAG", "Administrative info about test.example.com"]), ((1,None), "257", ["ADAAG", "A testing server in Test, USA"]), ((1,None), "258", ["ADAAG", "Administrator is tester"]), ((1,None), "259", ["ADAAG", "test@example.com"])], c.insight)
    
    def testAdminReplyIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackAdminInfo(((7,6), (1, None)))
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
    
    def testInfoReply(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackInfoRequest(((3,6), (1, None)))
        self.assertEquals([((1,None), "371", ["ADAAG", "I know 1 server and 1 user on 1 channel."]), ((1,None), "374", ["ADAAG", "End of /INFO list"])], c.insight)
    
    def testInfoReplyPlural(self):
        s = StateDouble()
        c = TestableConnection(s)
        s.users[(1,2)] = irc.state.user((1,2), "test2", "test", "example.com", [("+o", None)], 6, 0, 1234, "Joe Bloggs")
        s.servers[1].children = set([2])
        s.servers[2] = irc.state.server(1, 2, "test2.example.com", 1234, 1234, 1234, "P10", 0, [], "A test description")
        s.channels["#test2"] = irc.state.channel("#test2", 1234)
        c.callbackInfoRequest(((3,6), (1, None)))
        self.assertEquals([((1,None), "371", ["ADAAG", "I know 2 servers and 2 users on 2 channels."]), ((1,None), "374", ["ADAAG", "End of /INFO list"])], c.insight)
    
    def testInfoReplyIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackInfoRequest(((7,6), (1, None)))
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
    
    def testLusersReply(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackLusers(((3,6), (1, None), "Foo"))
        self.assertEquals([((1,None), "251", ["ADAAG", "There is 1 user on 1 server."]), ((1,None), "252", ["ADAAG", "0", "operators online."]), ((1,None), "254", ["ADAAG", "1", "channel formed."]), ((1,None), "255", ["ADAAG", "I have 1 client and 0 servers."])], c.insight)
    
    def testLusersReplyPlural(self):
        s = StateDouble()
        c = TestableConnection(s)
        s.users[(1,2)] = irc.state.user((1,2), "test2", "test", "example.com", [("+o", None)], 6, 0, 1234, "Joe Bloggs")
        s.servers[1].children = set([2])
        s.servers[2] = irc.state.server(1, 2, "test2.example.com", 1234, 1234, 1234, "P10", 0, [], "A test description")
        s.channels["#test2"] = irc.state.channel("#test2", 1234)
        c.callbackLusers(((3,6), (1, None), "Foo"))
        self.assertEquals([((1,None), "251", ["ADAAG", "There are 2 users on 2 servers."]), ((1,None), "252", ["ADAAG", "1", "operator online."]), ((1,None), "254", ["ADAAG", "2", "channels formed."]), ((1,None), "255", ["ADAAG", "I have 2 clients and 1 server."])], c.insight)
    
    def testLusersReplyIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackLusers(((7,6), (1, None), "Foo"))
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
    
    def testLinksReply(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackLinks(((3,6), (1, None), "*"))
        self.assertEquals([((1,None), "364", ["ADAAG", "test.example.com", "test.example.com", "0 P10 A test description"]), ((1,None), "365", ["ADAAG", "*", "End of /LINKS list."])], c.insight)
    
    def testLinksReplyLong(self):
        s = StateDouble()
        c = TestableConnection(s)
        s.servers[1].children = set([2])
        s.servers[2] = irc.state.server(1, 2, "test2.example.com", 1234, 1234, 1234, "P10", 0, [], "A test description2")
        s.servers[2].children = set([3])
        s.servers[3] = irc.state.server(2, 3, "test3.example.com", 1234, 1234, 1234, "P10", 0, [], "A test description3")
        c.callbackLinks(((3,6), (1, None), "*"))
        self.assertEquals([((1,None), "364", ["ADAAG", "test.example.com", "test.example.com", "0 P10 A test description"]), ((1,None), "364", ["ADAAG", "test2.example.com", "test.example.com", "0 P10 A test description2"]), ((1,None), "364", ["ADAAG", "test3.example.com", "test2.example.com", "0 P10 A test description3"]), ((1,None), "365", ["ADAAG", "*", "End of /LINKS list."])], c.insight)
    
    def testLinksReplyIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackLinks(((7,6), (1, None), "*"))
        self.assertEquals([], c.insight)
    
    def testLinksReplyMask(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackLinks(((3,6), (1, None), "*est.example.com"))
        self.assertEquals([((1,None), "364", ["ADAAG", "test.example.com", "test.example.com", "0 P10 A test description"]), ((1,None), "365", ["ADAAG", "*est.example.com", "End of /LINKS list."])], c.insight)
    
    def testLinksReplyIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callbackLinks(((3,6), (1, None), "foobar.example.com"))
        self.assertEquals([((1,None), "365", ["ADAAG", "foobar.example.com", "End of /LINKS list."])], c.insight)
    
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


def main():
    unittest.main()

if __name__ == '__main__':
    main()