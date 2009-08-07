#!/usr/bin/env python

import sys
import unittest
from test.irc.state import *
from test.p10.base64 import *
from test.p10.connection import *
from test.p10.parser import *
from test.p10.commands.account import *
from test.p10.commands.admin import *
from test.p10.commands.asll import *
from test.p10.commands.away import *
from test.p10.commands.burst import *
from test.p10.commands.clearmode import *
from test.p10.commands.connect import *
from test.p10.commands.create import *
from test.p10.commands.destruct import *
from test.p10.commands.desynch import *
from test.p10.commands.end_of_burst import *
from test.p10.commands.eob_ack import *
from test.p10.commands.error import *
from test.p10.commands.gline import *
from test.p10.commands.info import *
from test.p10.commands.invite import *
from test.p10.commands.join import *
from test.p10.commands.jupe import *
from test.p10.commands.kick import *
from test.p10.commands.kill import *
from test.p10.commands.links import *
from test.p10.commands.lusers import *
from test.p10.commands.mode import *
from test.p10.commands.motd import *
from test.p10.commands.names import *
from test.p10.commands.nick import *
from test.p10.commands.notice import *
from test.p10.commands.part import *
from test.p10.commands.password import *
from test.p10.commands.ping import *
from test.p10.commands.pong import *
from test.p10.commands.privmsg import *
from test.p10.commands.quit import *
from test.p10.commands.rping import *
from test.p10.commands.rpong import *
from test.p10.commands.server import *
from test.p10.commands.settime import *
from test.p10.commands.silence import *
from test.p10.commands.squit import *
from test.p10.commands.stats import *
from test.p10.commands.svsjoin import *
from test.p10.commands.svsnick import *
from test.p10.commands.time import *
from test.p10.commands.topic import *
from test.p10.commands.trace import *
from test.p10.commands.uping import *
from test.p10.commands.version import *
from test.p10.commands.wallchops import *
from test.p10.commands.wallops import *
from test.p10.commands.wallusers import *
from test.p10.commands.wallvoices import *
from test.p10.commands.who import *
from test.p10.commands.whois import *
from test.p10.commands.whowas import *

def main():
    unittest.main()

if __name__ == '__main__':
    main()