#!/usr/bin/env python

import unittest
from wish.p10.connection import Connection
from wish.irc.state import User, Server, Channel

class TestableConnection(Connection):
    
    def __init__(self, state):
        self.insight = []
        Connection.__init__(self, state)
        self.numeric = 2
    
    def _setup_callbacks(self):
        pass
    
    def _send_line(self, origin, command, args):
        self.insight.append((origin, command, args))
    
    def register_callback(self, callback, fn):
        pass
    
    def close_connection(self):
        self.connstate = self.COMPLETE

class StateDouble():
    
    def __init__(self):
        self.max_client_numerics = {1: 262143}
        self.users = dict({(1,1): User((1,1), "test", "test", "example.com", [], 6, 0, 1234, "Joe Bloggs")})
        self.servers = dict({1: Server(None, 1, "test.example.com", 1234, 1234, 1234, "P10", 0, [], "A test description")})
        self.channels = dict({"#test": Channel("#test", 1234)})
    
    @property
    def glines(self):
        return [("*!test@example.com", "A test description", 3600, True, 1000), ("*!test8@example.com", "Another test description", 3634, True, 1234), ("*!test3@example.com", "Inactive test description", 3634, False, 1234)]
    
    @property
    def jupes(self):
        return [("test.example.com", "A test description", 3600, True, 1000), ("test2.example.com", "Another test description", 3634, True, 1234), ("test9.example.com", "Inactive test description", 3634, False, 1234)]
    
    @property
    def server_id(self):
        return 1
    
    @property
    def server_name(self):
        return "test.example.com"
    
    @property
    def admin_name(self):
        return "tester"
    
    @property
    def contact_email(self):
        return "test@example.com"
    
    @property
    def server_description(self):
        return "A testing server in Test, USA"
    
    def get_next_hop(self, dest):
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
    
    @property
    def ts(self):
        return 1000

class ConnectionTest(unittest.TestCase):
    
    def testCanInit(self):
        s = StateDouble()
        c = TestableConnection(s)
    
    def testIntroduceServer(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_new_server((1, None), 8, "test.example.com", 262143, 1234, 1234, "P10", 1, "", "A testing server")
        self.assertEquals([((1, None), "S", ["test.example.com", "2", "1234", "1234", "P10", "AI]]]", "+", "A testing server"])], c.insight)
    
    def testIntroduceServerOnlyAppropriate(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_new_server((2, None), 3, "test.example.com", 262143, 1234, 1234, "P10", 1, "", "A testing server")
        c.callback_new_server((3, None), 12, "test2.example.com", 262143, 1234, 1234, "P10", 1, "", "A testing server")
        self.assertEquals([], c.insight)
    
    def testIntroduceUser(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_new_user((1, None), (1,2), "test", "test", "example.com", [], 1, 1, 1234, "A test user")
        self.assertEquals([((1, None), "N", ["test", "2", "1234", "test", "example.com", "AAAAAB", "ABAAC", "A test user"])], c.insight)
    
    def testIntroduceUserWithModes(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_new_user((1, None), (1,2), "test", "test", "example.com", [("+x", None)], 1, 1, 1234, "A test user")
        self.assertEquals([((1, None), "N", ["test", "2", "1234", "test", "example.com", "+x", "AAAAAB", "ABAAC", "A test user"])], c.insight)
    
    def testIntroduceUserWithModesAndArg(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_new_user((1, None), (1,2), "test", "test", "example.com", [("+r", "Test")], 1, 1, 1234, "A test user")
        self.assertEquals([((1, None), "N", ["test", "2", "1234", "test", "example.com", "+r", "Test", "AAAAAB", "ABAAC", "A test user"])], c.insight)
    
    def testIntroduceUserOnlyIfAppropriate(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_new_user((2, None), (2,2), "test", "test", "example.com", [("+r", "Test")], 1, 1, 1234, "A test user")
        self.assertEquals([], c.insight)
    
    def testChangeNick(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_change_nick((1, 6), (1,6), "test2", 68)
        self.assertEquals([((1,6), "N", ["test2", "68"])], c.insight)
    
    def testChangeNickSvs(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_change_nick((1, None), (1,6), "test2", 68)
        self.assertEquals([((1,None), "SN", ["ABAAG", "test2"])], c.insight)
    
    def testChangeNickIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_change_nick((2, 6), (2,6), "test2", 68)
        self.assertEquals([], c.insight)
    
    def testSquit(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_squit((4, None), (3, None), "Test Quit", 68)
        self.assertEquals([((4, None), "SQ", ["test3.example.com", "68", "Test Quit"])], c.insight)
    
    def testSquitIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_squit((2, None), (6, None), "Test Quit", 68)
        self.assertEquals([], c.insight)

    def testSquitMe(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_squit((1, None), (2, None), "Test Quit", 68)
        self.assertEquals([((1, None), "SQ", ["test.example.com", "0", "Test Quit"])], c.insight)
        self.assertEquals(c.COMPLETE, c.connstate)
    
    def testAuthenticate(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_authenticate((6, None), (1, 3), "example")
        self.assertEquals([((6, None), "AC", ["ABAAD", "example"])], c.insight)
    
    def testAuthenticateIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_authenticate((2, None), (1, 3), "example")
        self.assertEquals([], c.insight)
    
    def testAway(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_away((6, 3), "example")
        self.assertEquals([((6, 3), "A", ["example"])], c.insight)
    
    def testAwayIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_away((3, 3), "example")
        self.assertEquals([], c.insight)
    
    def testBack(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_back((6, 3))
        self.assertEquals([((6, 3), "A", [])], c.insight)
    
    def testBackIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_back((3, 3))
        self.assertEquals([], c.insight)
    
    def testCreate(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_channel_create((1, None), "#test", 1234)
        self.assertEquals([((1, None), "C", ["#test", "1234"])], c.insight)
    
    def testCreateIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_channel_create((3, None), "#test", 1234)
        self.assertEquals([], c.insight)
    
    def testJoin(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_channel_join((1, 6), (1, 6), "#test", "", 1234)
        self.assertEquals([((1, 6), "J", ["#test", "1234"])], c.insight)
    
    def testJoinIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_channel_join((3, 6), (3, 6), "#test", "", 1234)
        self.assertEquals([], c.insight)
    
    def testJoinSendModes(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_channel_join((1, 6), (1, 6), "#test", "ov", 1234)
        self.assertEquals([((1, 6), "J", ["#test", "1234"]), ((1,6), "M", ["#test", "+o", "ABAAG", "1234"]), ((1,6), "M", ["#test", "+v", "ABAAG", "1234"])], c.insight)
    
    def testSvsjoin(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_channel_join((1, None), (1, 6), "#test", "", 1234)
        self.assertEquals([((1, None), "SJ", ["ABAAG", "#test"])], c.insight)
    
    def testPart(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_channel_part((1, 6), "#test", "Reason")
        self.assertEquals([((1,6), "P", ["#test", "Reason"])], c.insight)
    
    def testPartIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_channel_part((3, 6), "#test", "Reason")
        self.assertEquals([], c.insight)
    
    def testPartAll(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_part_all((1, 6))
        self.assertEquals([((1,6), "J", ["0"])], c.insight)
    
    def testPartAllIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_part_all((3, 6))
        self.assertEquals([], c.insight)
    
    def testChannelChangeMode(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_channel_change_mode((1, 6), "#test", [("+c", None)])
        self.assertEquals([((1, 6), "M", ["#test", "+c", "1234"])], c.insight)
    
    def testChannelChangeModeIntArg(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_channel_change_mode((1, 6), "#test", [("+l", 7)])
        self.assertEquals([((1, 6), "M", ["#test", "+l", "7", "1234"])], c.insight)
    
    def testChannelChangeModeStringArg(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_channel_change_mode((1, 6), "#test", [("+k", "string")])
        self.assertEquals([((1, 6), "M", ["#test", "+k", "string", "1234"])], c.insight)
    
    def testChannelChangeMultiModeStringArg(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_channel_change_mode((1, 6), "#test", [("+C", None), ("+k", "string")])
        self.assertEquals([((1, 6), "M", ["#test", "+Ck", "string", "1234"])], c.insight)
    
    def testChannelChangeModeIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_channel_change_mode((2, 6), "#test", [("+c", None)])
        self.assertEquals([], c.insight)
    
    def testChannelAddBan(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_channel_add_ban((1, 6), "#test", "*!*@test.example.com")
        self.assertEquals([((1, 6), "M", ["#test", "+b", "*!*@test.example.com", "1234"])], c.insight)
    
    def testChannelAddBanIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_channel_add_ban((3, 6), "#test", "*!*@test.example.com")
        self.assertEquals([], c.insight)
    
    def testChannelRemoveBan(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_channel_remove_ban((1, 6), "#test", "*!*@test.example.com")
        self.assertEquals([((1, 6), "M", ["#test", "-b", "*!*@test.example.com", "1234"])], c.insight)
    
    def testChannelRemoveBanIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_channel_remove_ban((3, 6), "#test", "*!*@test.example.com")
        self.assertEquals([], c.insight)
    
    def testChannelClearBans(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_channel_clear_bans((1, 6), "#test")
        self.assertEquals([((1,6), "CM", ["#test", "b"])], c.insight)
    
    def testChannelClearBansIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_channel_clear_bans((2, 6), "#test")
        self.assertEquals([], c.insight)
    
    def testChannelChannelOp(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_channel_op((1, 6), "#test", (2, 3))
        self.assertEquals([((1, 6), "M", ["#test", "+o", "ACAAD", "1234"])], c.insight)
    
    def testChannelChannelOpIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_channel_op((3, 6), "#test", (2, 3))
        self.assertEquals([], c.insight)
    
    def testChannelChannelDeop(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_channel_deop((1, 6), "#test", (2,3))
        self.assertEquals([((1, 6), "M", ["#test", "-o", "ACAAD", "1234"])], c.insight)
    
    def testChannelChannelDeopIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_channel_deop((2, 6), "#test", (2,3))
        self.assertEquals([], c.insight)
    
    def testChannelClearOps(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_channel_clear_ops((1, 6), "#test")
        self.assertEquals([((1,6), "CM", ["#test", "o"])], c.insight)
    
    def testChannelClearOpsIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_channel_clear_ops((2, 6), "#test")
        self.assertEquals([], c.insight)
    
    def testChannelChannelVoice(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_channel_voice((1, 6), "#test", (2, 3))
        self.assertEquals([((1, 6), "M", ["#test", "+v", "ACAAD", "1234"])], c.insight)
    
    def testChannelChannelVoiceIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_channel_voice((3, 6), "#test", (2, 3))
        self.assertEquals([], c.insight)
    
    def testChannelChannelDevoice(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_channel_devoice((1, 6), "#test", (2,3))
        self.assertEquals([((1, 6), "M", ["#test", "-v", "ACAAD", "1234"])], c.insight)
    
    def testChannelChannelDevoiceIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_channel_devoice((2, 6), "#test", (2,3))
        self.assertEquals([], c.insight)
    
    def testChannelClearVoices(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_channel_clear_voices((1, 6), "#test")
        self.assertEquals([((1,6), "CM", ["#test", "v"])], c.insight)
    
    def testChannelClearVoicesIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_channel_clear_voices((2, 6), "#test")
        self.assertEquals([], c.insight)
    
    def testGlineAdd(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_gline_add((1, None), "*!test@example.com", None, 3600, "A test description")
        self.assertEquals([((1, None), "GL", ["*", "+*!test@example.com", "2600", "1000", "A test description"])], c.insight)
    
    def testGlineAddIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_gline_add((2, None), "*!test@example.com", None, 2400, "A test description")
        self.assertEquals([], c.insight)
    
    def testGlineAddTarget(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_gline_add((1, None), "*!test@example.com", 3, 3600, "A test description")
        self.assertEquals([((1, None), "GL", ["AD", "+*!test@example.com", "2600", "1000", "A test description"])], c.insight)
    
    def testGlineAddTargetIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_gline_add((1, None), "*!test@example.com", 9, 2400, "A test description")
        self.assertEquals([], c.insight)
    
    def testGlineRemove(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_gline_remove((1, None), "*!test@example.com", None)
        self.assertEquals([((1, None), "GL", ["*", "-*!test@example.com", "2600", "1000", "A test description"])], c.insight)
    
    def testGlineRemoveIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_gline_remove((3, None), "*!test@example.com", None)
        self.assertEquals([], c.insight)
    
    def testGlineRemoveTarget(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_gline_remove((1, None), "*!test@example.com", 2)
        self.assertEquals([((1, None), "GL", ["AC", "-*!test@example.com", "2600", "1000", "A test description"])], c.insight)
    
    def testGlineRemoveTargetIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_gline_remove((1, None), "*!test@example.com", 8)
        self.assertEquals([], c.insight)
    
    def testInvite(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_invite((1, 6), (3, 2), "#test")
        self.assertEquals([((1,6), "I", ["test", "#test"])], c.insight)
    
    def testInviteIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_invite((1, 6), (7, 1), "#test")
        self.assertEquals([], c.insight)
    
    def testJupeAdd(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_jupe_add((1, None), "test.example.com", None, 3600, "A test description")
        self.assertEquals([((1, None), "JU", ["*", "+test.example.com", "2600", "1000", "A test description"])], c.insight)
    
    def testJupeAddIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_jupe_add((2, None), "test.example.com", None, 2400, "A test description")
        self.assertEquals([], c.insight)
    
    def testJupeAddTarget(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_jupe_add((1, None), "test.example.com", 3, 3600, "A test description")
        self.assertEquals([((1, None), "JU", ["AD", "+test.example.com", "2600", "1000", "A test description"])], c.insight)
    
    def testJupeAddTargetIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_jupe_add((1, None), "test.example.com", 9, 2400, "A test description")
        self.assertEquals([], c.insight)
    
    def testJupeRemove(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_jupe_remove((1, None), "test.example.com", None)
        self.assertEquals([((1, None), "JU", ["*", "-test.example.com", "2600", "1000", "A test description"])], c.insight)
    
    def testJupeRemoveIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_jupe_remove((3, None), "test.example.com", None)
        self.assertEquals([], c.insight)
    
    def testJupeRemoveTarget(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_jupe_remove((1, None), "test.example.com", 2)
        self.assertEquals([((1, None), "JU", ["AC", "-test.example.com", "2600", "1000", "A test description"])], c.insight)
    
    def testJupeRemoveTargetIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_jupe_remove((1, None), "test.example.com", 8)
        self.assertEquals([], c.insight)
    
    def testAdminSend(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_admin_info((1,6), (3, None))
        self.assertEquals([((1,6), "AD", ["AD"])], c.insight)
    
    def testAdminSendIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_admin_info((1,6), (7, None))
        self.assertEquals([], c.insight)
    
    def testInfoSend(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_info_request((1,6), (3, None))
        self.assertEquals([((1,6), "F", ["AD"])], c.insight)
    
    def testInfoSendIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_info_request((1,6), (7, None))
        self.assertEquals([], c.insight)
    
    def testKick(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_kick((1, 6), "#test", (5,2), "A reason")
        self.assertEquals([((1,6), "K", ["#test", "AFAAC", "A reason"])], c.insight)
    
    def testKickIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_kick((3, 6), "#test", (5,2), "A reason")
        self.assertEquals([], c.insight)
    
    def testZombiePart(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_zombie_part((1, 6), "#test")
        self.assertEquals([((1,6), "P", ["#test", "Zombie parting channel"])], c.insight)
    
    def testZombiePartIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_zombie_part((3, 6), "#test")
        self.assertEquals([], c.insight)
    
    def testDestruct(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_channel_destroy((1, 6), "#test", 1234)
        self.assertEquals([((1,6), "DE", ["#test", "1234"])], c.insight)
    
    def testDestructIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_channel_destroy((3, 6), "#test", 1234)
        self.assertEquals([], c.insight)
    
    def testQuit(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_quit((1, 6), "Quitting network", False)
        self.assertEquals([((1,6), "Q", ["Quitting network"])], c.insight)
    
    def testQuitIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_quit((3, 6), "Quitting network", False)
        self.assertEquals([], c.insight)
    
    def testQuitOnlyPropagatedIfNotSquit(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_quit((1, 6), "Quitting network", True)
        self.assertEquals([], c.insight)
    
    def testKill(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_kill((1, 6), (3,6), ["test.example.com", "origin.example.com"], "Being naughty")
        self.assertEquals([((1,6), "D", ["ADAAG", "test.example.com!origin.example.com (Being naughty)"])], c.insight)
    
    def testKillIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_kill((1, 6), (5,6), "test.example.com", "Being naughty")
        self.assertEquals([], c.insight)
    
    def testLusersSend(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_lusers((1,6), (3, None), "Foo")
        self.assertEquals([((1,6), "LU", ["Foo", "AD"])], c.insight)
    
    def testLusersSendIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_lusers((1,6), (7, None), "Foo")
        self.assertEquals([], c.insight)
    
    def testLinksSend(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_links((1,6), (3, None), "*")
        self.assertEquals([((1,6), "LI", ["AD", "*"])], c.insight)
    
    def testLinksSendIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_links((1,6), (7, None), "*")
        self.assertEquals([], c.insight)
    
    def testUserChangeMode(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_change_user_mode((1, 6), [("+c", None)])
        self.assertEquals([((1, 6), "M", ["localtest", "+c"])], c.insight)
    
    def testUserChangeModeIntArg(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_change_user_mode((1, 6), [("+l", 7)])
        self.assertEquals([((1, 6), "M", ["localtest", "+l", "7"])], c.insight)
    
    def testUserChangeModeStringArg(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_change_user_mode((1, 6), [("+k", "string")])
        self.assertEquals([((1, 6), "M", ["localtest", "+k", "string"])], c.insight)
    
    def testUserChangeMultiModeStringArg(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_change_user_mode((1, 6), [("+C", None), ("+k", "string")])
        self.assertEquals([((1, 6), "M", ["localtest", "+Ck", "string"])], c.insight)
    
    def testUserChangeModeIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_change_user_mode((2, 6), [("+c", None)])
        self.assertEquals([], c.insight)
    
    def testMOTDSend(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_motd((1,6), (3, None))
        self.assertEquals([((1,6), "MO", ["AD"])], c.insight)
    
    def testMOTDSendIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_motd((1,6), (7, None))
        self.assertEquals([], c.insight)
    
    def testNamesSend(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_names((1,6), (3, None), ["#test"])
        self.assertEquals([((1,6), "E", ["#test", "AD"])], c.insight)
    
    def testNamesSendIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_names((1,6), (7, None), ["#test"])
        self.assertEquals([], c.insight)
    
    def testTopic(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_topic((1,6), "#test", "New topic", 1234, 12345)
        self.assertEquals([((1,6), "T", ["#test", "12345", "1234", "New topic"])], c.insight)
    
    def testTopicIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_topic((2,6), "#test", "New topic", 1234, 1234)
        self.assertEquals([], c.insight)
    
    def testSilenceAdd(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_silence_add((1,6), "*@example.com")
        self.assertEquals([((1,6), "U", ["*", "*@example.com"])], c.insight)
    
    def testSilenceAddIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_silence_add((2,6), "*@example.com")
        self.assertEquals([], c.insight)
    
    def testSilenceAdd(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_silence_remove((1,6), "*@example.com")
        self.assertEquals([((1,6), "U", ["*", "-*@example.com"])], c.insight)
    
    def testSilenceAddIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_silence_remove((2,6), "*@example.com")
        self.assertEquals([], c.insight)
    
    def testVersionSend(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_request_version((1,6), (3, None))
        self.assertEquals([((1,6), "V", ["AD"])], c.insight)
    
    def testVersionSendIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_request_version((1,6), (7, None))
        self.assertEquals([], c.insight)
    
    def testOobmsg(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_oobmsg((1, None), (3,6), "123", ["Arg1", "Arg 2"])
        self.assertEquals([((1, None), "123", ["ADAAG", "Arg1", "Arg 2"])], c.insight)
    
    def testOobmsgIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_oobmsg((1, None), (6,6), "123", ["Arg1", "Arg 2"])
        self.assertEquals([], c.insight)
    
    def testPingSend(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_ping((1, None), "test", (3, None))
        self.assertEquals([((1,None), "G", ["test", "AD"])], c.insight)
    
    def testPingSendIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_ping((1, None), "test", (7, None))
        self.assertEquals([], c.insight)
    
    def testPingReply(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_ping((3, None), "test", (1, None))
        self.assertEquals([((1,None), "Z", ["AB", "test"])], c.insight)
    
    def testPingReplyIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_ping((7, None), "test", (1, None))
        self.assertEquals([], c.insight)
    
    def testPongSend(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_pong((1, None), (1, None), (3, None))
        self.assertEquals([((1,None), "Z", ["AB", "AD"])], c.insight)
    
    def testPongSendIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_pong((1, None), "test", (7, None))
        self.assertEquals([], c.insight)
    
    def testWallusers(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_wallusers((6,2), "A message")
        self.assertEquals([((6,2), "WU", ["A message"])], c.insight)
    
    def testWallusersIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_wallusers((3,2), "A message")
        self.assertEquals([], c.insight)
    
    def testWallops(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_wallops((6,2), "A message")
        self.assertEquals([((6,2), "WA", ["A message"])], c.insight)
    
    def testWallopsIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_wallops((3,2), "A message")
        self.assertEquals([], c.insight)
    
    def testWallvoices(self):
        s = StateDouble()
        c = TestableConnection(s)
        s.channels["#test"].join((3,2), "v")
        c.callback_wallvoices((1, 6), "#test", "A message")
        self.assertEquals([((1,6), "WV", ["#test", "A message"])], c.insight)
    
    def testWallvoicesIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        s.channels["#test"].join((3,2), "v")
        c.callback_wallvoices((3, 6), "#test", "A message")
        self.assertEquals([], c.insight)
    
    def testWallvoicesIfSpecific(self):
        s = StateDouble()
        c = TestableConnection(s)
        s.channels["#test"].join((3,2), "")
        c.callback_wallvoices((1, 6), "#test", "A message")
        self.assertEquals([], c.insight)
    
    def testWallvoicesIfOp(self):
        s = StateDouble()
        c = TestableConnection(s)
        s.channels["#test"].join((3,2), "o")
        c.callback_wallvoices((1, 6), "#test", "A message")
        self.assertEquals([((1,6), "WV", ["#test", "A message"])], c.insight)
    
    def testWallvoicesOnlyOnce(self):
        s = StateDouble()
        c = TestableConnection(s)
        s.channels["#test"].join((3,2), "v")
        s.channels["#test"].join((3,9), "o")
        c.callback_wallvoices((1, 6), "#test", "A message")
        self.assertEquals([((1,6), "WV", ["#test", "A message"])], c.insight)
    
    def testWallchops(self):
        s = StateDouble()
        c = TestableConnection(s)
        s.channels["#test"].join((3,2), "o")
        c.callback_wallchops((1, 6), "#test", "A message")
        self.assertEquals([((1,6), "WC", ["#test", "A message"])], c.insight)
    
    def testWallchopsIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        s.channels["#test"].join((3,2), "o")
        c.callback_wallchops((3, 6), "#test", "A message")
        self.assertEquals([], c.insight)
    
    def testWallchopsIfSpecific(self):
        s = StateDouble()
        c = TestableConnection(s)
        s.channels["#test"].join((3,2), "")
        c.callback_wallchops((1, 6), "#test", "A message")
        self.assertEquals([], c.insight)
    
    def testWallchopsExcludesVoice(self):
        s = StateDouble()
        c = TestableConnection(s)
        s.channels["#test"].join((3,2), "v")
        c.callback_wallchops((1, 6), "#test", "A message")
        self.assertEquals([], c.insight)
    
    def testWallchopsOnlyOnce(self):
        s = StateDouble()
        c = TestableConnection(s)
        s.channels["#test"].join((3,2), "o")
        s.channels["#test"].join((3,9), "o")
        c.callback_wallchops((1, 6), "#test", "A message")
        self.assertEquals([((1,6), "WC", ["#test", "A message"])], c.insight)
    
    def testWhoisSend(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_request_whois((1,6), (3, None), "test")
        self.assertEquals([((1,6), "W", ["AD", "test"])], c.insight)
    
    def testWhoisSendIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_request_whois((1,6), (7, None), "test")
        self.assertEquals([], c.insight)
    
    def testTraceSend(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_trace((1,6), "test", (3, None))
        self.assertEquals([((1,6), "TR", ["test", "AD"])], c.insight)
    
    def testTraceSendIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_trace((1,6), "test", (7, None))
        self.assertEquals([], c.insight)
    
    def testStatsSend(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_request_stats((1,6), (3, None), "B", "Search")
        self.assertEquals([((1,6), "R", ["B", "AD", "Search"])], c.insight)
    
    def testStatsSendNoExtra(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_request_stats((1,6), (3, None), "B", None)
        self.assertEquals([((1,6), "R", ["B", "AD"])], c.insight)
    
    def testStatsSendIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_request_stats((1,6), (7, None), "B", None)
        self.assertEquals([], c.insight)
    
    def testPrivmsgPerson(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_privmsg((1, 6), (3,1), "A message")
        self.assertEquals([((1,6), "P", ["ADAAB", "A message"])], c.insight)
    
    def testPrivmsgPersonIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_privmsg((1, 6), (9,1), "A message")
        self.assertEquals([], c.insight)
    
    def testPrivmsgLong(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_privmsg((1, 6), "test@test2.example.com", "A message")
        self.assertEquals([((1,6), "P", ["test@test2.example.com", "A message"])], c.insight)
    
    def testPrivmsgLongIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_privmsg((1, 6), "test@test9.example.com", "A message")
        self.assertEquals([], c.insight)
    
    def testPrivmsgChannel(self):
        s = StateDouble()
        c = TestableConnection(s)
        s.channels["#test"].join((3,2), "")
        c.callback_privmsg((1, 6), "#test", "A message")
        self.assertEquals([((1,6), "P", ["#test", "A message"])], c.insight)
    
    def testPrivmsgChannelIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        s.channels["#test"].join((3,2), "")
        c.callback_privmsg((3, 6), "#test", "A message")
        self.assertEquals([], c.insight)
    
    def testPrivmsgChannelIfSpecific(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_privmsg((1, 6), "#test", "A message")
        self.assertEquals([], c.insight)
    
    def testPrivmsgServer(self):
        s = StateDouble()
        c = TestableConnection(s)
        s.servers[2] = Server(1, 2, "test2.example.com", 1234, 1234, 1234, "P10", 0, [], "A test description")
        c.callback_privmsg((1,6), "$test2.example.com", "A message")
        self.assertEquals([((1,6), "P", ["$test2.example.com", "A message"])], c.insight)
    
    def testPrivmsgServerIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        s.servers[9] = Server(1, 9, "test9.example.com", 1234, 1234, 1234, "P10", 0, [], "A test description")
        c.callback_privmsg((1,6), "$test9.example.com", "A message")
        self.assertEquals([], c.insight)
    
    def testPrivmsgServerMask(self):
        s = StateDouble()
        c = TestableConnection(s)
        s.servers[2] = Server(1, 2, "test2.example.com", 1234, 1234, 1234, "P10", 0, [], "A test description")
        c.callback_privmsg((1,6), "$test*.example.com", "A message")
        self.assertEquals([((1,6), "P", ["$test*.example.com", "A message"])], c.insight)
    
    def testNoticePerson(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_notice((1, 6), (3,1), "A message")
        self.assertEquals([((1,6), "O", ["ADAAB", "A message"])], c.insight)
    
    def testNoticePersonIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_notice((1, 6), (9,1), "A message")
        self.assertEquals([], c.insight)
    
    def testNoticeLong(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_notice((1, 6), "test@test2.example.com", "A message")
        self.assertEquals([((1,6), "O", ["test@test2.example.com", "A message"])], c.insight)
    
    def testNoticeLongIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_notice((1, 6), "test@test9.example.com", "A message")
        self.assertEquals([], c.insight)
    
    def testNoticeChannel(self):
        s = StateDouble()
        c = TestableConnection(s)
        s.channels["#test"].join((3,2), "")
        c.callback_notice((1, 6), "#test", "A message")
        self.assertEquals([((1,6), "O", ["#test", "A message"])], c.insight)
    
    def testNoticeChannelIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        s.channels["#test"].join((3,2), "")
        c.callback_notice((3, 6), "#test", "A message")
        self.assertEquals([], c.insight)
    
    def testNoticeChannelIfSpecific(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.callback_notice((1, 6), "#test", "A message")
        self.assertEquals([], c.insight)
    
    def testNoticeServer(self):
        s = StateDouble()
        c = TestableConnection(s)
        s.servers[2] = Server(1, 2, "test2.example.com", 1234, 1234, 1234, "P10", 0, [], "A test description")
        c.callback_notice((1,6), "$test2.example.com", "A message")
        self.assertEquals([((1,6), "O", ["$test2.example.com", "A message"])], c.insight)
    
    def testNoticeServerIfRelevant(self):
        s = StateDouble()
        c = TestableConnection(s)
        s.servers[9] = Server(1, 9, "test9.example.com", 1234, 1234, 1234, "P10", 0, [], "A test description")
        c.callback_notice((1,6), "$test9.example.com", "A message")
        self.assertEquals([], c.insight)
    
    def testNoticeServerMask(self):
        s = StateDouble()
        c = TestableConnection(s)
        s.servers[2] = Server(1, 2, "test2.example.com", 1234, 1234, 1234, "P10", 0, [], "A test description")
        c.callback_notice((1,6), "$test*.example.com", "A message")
        self.assertEquals([((1,6), "O", ["$test*.example.com", "A message"])], c.insight)
    
    def testSendBurst(self):
        s = StateDouble()
        c = TestableConnection(s)
        s.servers[9] = Server(1, 9, "test9.example.com", 262143, 1234, 1234, "P10", 0, [], "A test description")
        s.servers[1].add_child(9)
        c._send_burst()
        self.assertEquals([
            ((1, None), "S", ["test9.example.com", "1", "1234", "1234", "P10", "AJ]]]", "+", "A test description"]),
            ((1, None), "GL", ["*", "+*!test@example.com", "2600", "1000", "A test description"]),
            ((1, None), "GL", ["*", "+*!test8@example.com", "2400", "1234", "Another test description"]),
            ((1, None), "GL", ["*", "-*!test3@example.com", "2400", "1234", "Inactive test description"]),
            ((1, None), "JU", ["*", "+test.example.com", "2600", "1000", "A test description"]),
            ((1, None), "JU", ["*", "+test2.example.com", "2400", "1234", "Another test description"]),
            ((1, None), "JU", ["*", "-test9.example.com", "2400", "1234", "Inactive test description"]),
            ((1, None), "N", ["test", "1", "1234", "test", "example.com", "AAAAAG", "ABAAB", "Joe Bloggs"]),
            ((1, None), "B", ["#test", "1234"]),
            ((1, None), "EB", [])], c.insight)
    
    def testSendBurstNotBackToSelf(self):
        s = StateDouble()
        c = TestableConnection(s)
        c.numeric = 9
        s.servers[9] = Server(1, 9, "test9.example.com", 262143, 1234, 1234, "P10", 0, [], "A test description")
        s.servers[1].add_child(9)
        c._send_burst()
        self.assertEquals([
            ((1, None), "GL", ["*", "+*!test@example.com", "2600", "1000", "A test description"]),
            ((1, None), "GL", ["*", "+*!test8@example.com", "2400", "1234", "Another test description"]),
            ((1, None), "GL", ["*", "-*!test3@example.com", "2400", "1234", "Inactive test description"]),
            ((1, None), "JU", ["*", "+test.example.com", "2600", "1000", "A test description"]),
            ((1, None), "JU", ["*", "+test2.example.com", "2400", "1234", "Another test description"]),
            ((1, None), "JU", ["*", "-test9.example.com", "2400", "1234", "Inactive test description"]),
            ((1, None), "N", ["test", "1", "1234", "test", "example.com", "AAAAAG", "ABAAB", "Joe Bloggs"]),
            ((1, None), "B", ["#test", "1234"]),
            ((1, None), "EB", [])], c.insight)
    
    def testSendBurstChannelModes(self):
        s = StateDouble()
        c = TestableConnection(s)
        s.channels["#test"].change_mode(("+c", None))
        s.channels["#test"].change_mode(("+i", None))
        s.channels["#test"].change_mode(("+l", 28))
        c._send_burst()
        self.assertEquals([
            ((1, None), "GL", ["*", "+*!test@example.com", "2600", "1000", "A test description"]),
            ((1, None), "GL", ["*", "+*!test8@example.com", "2400", "1234", "Another test description"]),
            ((1, None), "GL", ["*", "-*!test3@example.com", "2400", "1234", "Inactive test description"]),
            ((1, None), "JU", ["*", "+test.example.com", "2600", "1000", "A test description"]),
            ((1, None), "JU", ["*", "+test2.example.com", "2400", "1234", "Another test description"]),
            ((1, None), "JU", ["*", "-test9.example.com", "2400", "1234", "Inactive test description"]),
            ((1, None), "N", ["test", "1", "1234", "test", "example.com", "AAAAAG", "ABAAB", "Joe Bloggs"]),
            ((1, None), "B", ["#test", "1234", "+icl", "28"]),
            ((1, None), "EB", [])], c.insight)
    
    def testSendBurstChannelUsers(self):
        s = StateDouble()
        c = TestableConnection(s)
        s.channels["#test"].join((1,1), "ov")
        s.channels["#test"].join((1,2), "o")
        s.channels["#test"].join((1,3), "o")
        s.channels["#test"].join((1,4), "v")
        s.channels["#test"].join((1,5), "v")
        s.channels["#test"].join((1,8), "")
        s.channels["#test"].join((1,10), "")
        c._send_burst()
        self.assertEquals([
            ((1, None), "GL", ["*", "+*!test@example.com", "2600", "1000", "A test description"]),
            ((1, None), "GL", ["*", "+*!test8@example.com", "2400", "1234", "Another test description"]),
            ((1, None), "GL", ["*", "-*!test3@example.com", "2400", "1234", "Inactive test description"]),
            ((1, None), "JU", ["*", "+test.example.com", "2600", "1000", "A test description"]),
            ((1, None), "JU", ["*", "+test2.example.com", "2400", "1234", "Another test description"]),
            ((1, None), "JU", ["*", "-test9.example.com", "2400", "1234", "Inactive test description"]),
            ((1, None), "N", ["test", "1", "1234", "test", "example.com", "AAAAAG", "ABAAB", "Joe Bloggs"]),
            ((1, None), "B", ["#test", "1234", "ABAAK,ABAAI,ABAAE:v,ABAAF,ABAAD:o,ABAAC,ABAAB:ov"]),
            ((1, None), "EB", [])], c.insight)
    
    def testSendBurstChannelBans(self):
        s = StateDouble()
        c = TestableConnection(s)
        s.channels["#test"].add_ban("test!test@example.com")
        s.channels["#test"].add_ban("test5!t3st@example2.com")
        c._send_burst()
        self.assertEquals([
            ((1, None), "GL", ["*", "+*!test@example.com", "2600", "1000", "A test description"]),
            ((1, None), "GL", ["*", "+*!test8@example.com", "2400", "1234", "Another test description"]),
            ((1, None), "GL", ["*", "-*!test3@example.com", "2400", "1234", "Inactive test description"]),
            ((1, None), "JU", ["*", "+test.example.com", "2600", "1000", "A test description"]),
            ((1, None), "JU", ["*", "+test2.example.com", "2400", "1234", "Another test description"]),
            ((1, None), "JU", ["*", "-test9.example.com", "2400", "1234", "Inactive test description"]),
            ((1, None), "N", ["test", "1", "1234", "test", "example.com", "AAAAAG", "ABAAB", "Joe Bloggs"]),
            ((1, None), "B", ["#test", "1234", "%test5!t3st@example2.com test!test@example.com"]),
            ((1, None), "EB", [])], c.insight)
    
    def testSendBurstServersInOrder(self):
        s = StateDouble()
        c = TestableConnection(s)
        s.servers[9] = Server(1, 9, "test9.example.com", 262143, 1234, 1234, "P10", 1, [], "A test description")
        s.servers[1].add_child(9)
        s.servers[10] = Server(1, 10, "test10.example.com", 262143, 1234, 1234, "P10", 1, [], "A test description 2")
        s.servers[1].add_child(10)
        s.servers[13] = Server(10, 13, "test13.example.com", 262143, 1234, 1234, "P10", 2, [], "A test description 3")
        s.servers[10].add_child(13)
        s.servers[14] = Server(13, 14, "test14.example.com", 262143, 1234, 1234, "P10", 3, [], "A test description 4")
        s.servers[13].add_child(14)
        c._send_burst()
        self.assertEquals([
            ((1, None), "S", ["test9.example.com", "2", "1234", "1234", "P10", "AJ]]]", "+", "A test description"]),
            ((1, None), "S", ["test10.example.com", "2", "1234", "1234", "P10", "AK]]]", "+", "A test description 2"]),
            ((10, None), "S", ["test13.example.com", "3", "1234", "1234", "P10", "AN]]]", "+", "A test description 3"]),
            ((13, None), "S", ["test14.example.com", "4", "1234", "1234", "P10", "AO]]]", "+", "A test description 4"]),
            ((1, None), "GL", ["*", "+*!test@example.com", "2600", "1000", "A test description"]),
            ((1, None), "GL", ["*", "+*!test8@example.com", "2400", "1234", "Another test description"]),
            ((1, None), "GL", ["*", "-*!test3@example.com", "2400", "1234", "Inactive test description"]),
            ((1, None), "JU", ["*", "+test.example.com", "2600", "1000", "A test description"]),
            ((1, None), "JU", ["*", "+test2.example.com", "2400", "1234", "Another test description"]),
            ((1, None), "JU", ["*", "-test9.example.com", "2400", "1234", "Inactive test description"]),
            ((1, None), "N", ["test", "1", "1234", "test", "example.com", "AAAAAG", "ABAAB", "Joe Bloggs"]),
            ((1, None), "B", ["#test", "1234"]),
            ((1, None), "EB", [])], c.insight)
    
    def testSendBurstMultiLineChannels(self):
        # Lines headers have 16 (494 chars left)
        # This test is terrible. It does check what's being output is actually correct
        s = StateDouble()
        c = TestableConnection(s)
        s.channels["#test"].change_mode(("+c", None)) # +2 18/492
        s.channels["#test"].change_mode(("+i", None)) # +1 19/491
        s.channels["#test"].change_mode(("+l", 28)) # +4 23/487
        s.channels["#test"].join((1,1), "ov") # +9
        s.channels["#test"].join((1,2), "o") # +8
        s.channels["#test"].join((1,3), "o") # +8
        s.channels["#test"].join((1,4), "v") # +8
        s.channels["#test"].join((1,5), "v") # +8
        
        for i in range(8, 151):
            s.channels["#test"].join((1,i), "")
        for i in range(1, 20):
            s.channels["#test"].add_ban("test" + str(i) + "!test@example.com")
        
        c._send_burst()
        
        for line in c.insight:
            self.failIf(len(" ".join(line[2])) > 505, len(" ".join(line[2])))


def main():
    unittest.main()

if __name__ == '__main__':
    main()
