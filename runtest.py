#!/usr/bin/env python

import sys
import unittest
import test.p10.parser
import test.p10.base64
import test.p10.state
import test.p10.commands.account
import test.p10.commands.admin
import test.p10.commands.asll
import test.p10.commands.away
import test.p10.commands.burst
import test.p10.commands.clearmode
import test.p10.commands.close
import test.p10.commands.cnotice
import test.p10.commands.connect
import test.p10.commands.cprivmsg
import test.p10.commands.create
import test.p10.commands.destruct
import test.p10.commands.desynch
import test.p10.commands.die
import test.p10.commands.dns
import test.p10.commands.end_of_burst
import test.p10.commands.eob_ack
import test.p10.commands.error
import test.p10.commands.get
import test.p10.commands.gline
import test.p10.commands.hash
import test.p10.commands.help
import test.p10.commands.info
import test.p10.commands.invite
import test.p10.commands.ison
import test.p10.commands.join
import test.p10.commands.jupe
import test.p10.commands.kick
import test.p10.commands.kill
import test.p10.commands.links
import test.p10.commands.list
import test.p10.commands.lusers
import test.p10.commands.map
import test.p10.commands.mode
import test.p10.commands.motd
import test.p10.commands.names
import test.p10.commands.nick
import test.p10.commands.notice
import test.p10.commands.oper
import test.p10.commands.opmode
import test.p10.commands.part
import test.p10.commands.password
import test.p10.commands.ping
import test.p10.commands.pong
import test.p10.commands.post
import test.p10.commands.privmsg
import test.p10.commands.privs
import test.p10.commands.proto
import test.p10.commands.quit
import test.p10.commands.rehash
import test.p10.commands.reset
import test.p10.commands.restart
import test.p10.commands.rping
import test.p10.commands.rpong
import test.p10.commands.server
import test.p10.commands.set
import test.p10.commands.settime
import test.p10.commands.silence
import test.p10.commands.squit
import test.p10.commands.stats
import test.p10.commands.svsjoin
import test.p10.commands.svsnick
import test.p10.commands.time
import test.p10.commands.topic
import test.p10.commands.trace
import test.p10.commands.uping
import test.p10.commands.user
import test.p10.commands.userhost
import test.p10.commands.userip
import test.p10.commands.version
import test.p10.commands.wallchops
import test.p10.commands.wallops
import test.p10.commands.wallusers
import test.p10.commands.wallvoices
import test.p10.commands.who
import test.p10.commands.whois
import test.p10.commands.whowas

def main():
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.parser))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.base64))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.state))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.account))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.asll))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.away))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.burst))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.clearmode))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.close))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.cnotice))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.connect))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.cprivmsg))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.create))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.destruct))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.desynch))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.die))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.dns))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.end_of_burst))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.eob_ack))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.error))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.get))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.gline))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.hash))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.help))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.info))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.invite))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.ison))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.join))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.jupe))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.kick))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.kill))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.links))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.list))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.lusers))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.map))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.mode))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.motd))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.names))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.nick))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.notice))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.oper))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.opmode))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.part))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.password))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.ping))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.pong))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.post))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.privmsg))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.privs))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.proto))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.quit))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.rehash))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.reset))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.restart))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.rping))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.rpong))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.server))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.set))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.settime))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.silence))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.squit))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.stats))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.svsjoin))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.svsnick))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.time))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.topic))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.trace))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.uping))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.user))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.userhost))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.userip))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.version))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.wallchops))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.wallops))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.wallusers))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.wallvoices))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.who))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.whois))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.whowas))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if result.wasSuccessful():
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()