#!/usr/bin/env python

import unittest

from wish.test.irc.admin import *
from wish.test.irc.info import *
from wish.test.irc.links import *
from wish.test.irc.lusers import *
from wish.test.irc.motd import *
from wish.test.irc.names import *
from wish.test.irc.state import *
from wish.test.irc.version import *
from wish.test.p10.base64 import *
from wish.test.p10.connection import *
from wish.test.p10.parser import *
from wish.test.p10.commands.account import *
from wish.test.p10.commands.admin import *
from wish.test.p10.commands.asll import *
from wish.test.p10.commands.away import *
from wish.test.p10.commands.burst import *
from wish.test.p10.commands.clearmode import *
from wish.test.p10.commands.connect import *
from wish.test.p10.commands.create import *
from wish.test.p10.commands.destruct import *
from wish.test.p10.commands.end_of_burst import *
from wish.test.p10.commands.eob_ack import *
from wish.test.p10.commands.error import *
from wish.test.p10.commands.gline import *
from wish.test.p10.commands.info import *
from wish.test.p10.commands.invite import *
from wish.test.p10.commands.join import *
from wish.test.p10.commands.jupe import *
from wish.test.p10.commands.kick import *
from wish.test.p10.commands.kill import *
from wish.test.p10.commands.links import *
from wish.test.p10.commands.lusers import *
from wish.test.p10.commands.mode import *
from wish.test.p10.commands.motd import *
from wish.test.p10.commands.names import *
from wish.test.p10.commands.nick import *
from wish.test.p10.commands.notice import *
from wish.test.p10.commands.numberrelay import *
from wish.test.p10.commands.part import *
from wish.test.p10.commands.password import *
from wish.test.p10.commands.ping import *
from wish.test.p10.commands.pong import *
from wish.test.p10.commands.privmsg import *
from wish.test.p10.commands.quit import *
from wish.test.p10.commands.rping import *
from wish.test.p10.commands.rpong import *
from wish.test.p10.commands.server import *
from wish.test.p10.commands.settime import *
from wish.test.p10.commands.silence import *
from wish.test.p10.commands.squit import *
from wish.test.p10.commands.stats import *
from wish.test.p10.commands.svsjoin import *
from wish.test.p10.commands.svsnick import *
from wish.test.p10.commands.time import *
from wish.test.p10.commands.topic import *
from wish.test.p10.commands.trace import *
from wish.test.p10.commands.uping import *
from wish.test.p10.commands.version import *
from wish.test.p10.commands.wallchops import *
from wish.test.p10.commands.wallops import *
from wish.test.p10.commands.wallusers import *
from wish.test.p10.commands.wallvoices import *
from wish.test.p10.commands.whois import *
from wish.test.p10.commands.whowas import *

def main():
    unittest.main()

if __name__ == '__main__':
    main()
