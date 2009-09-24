#!/usr/bin/env python
#
# WISH
# WorldIRC Service Host
#

class WISHConfig:
    
    # Please set the name of this server here
    serverName = "beta.worldirc.org"
    
    # A description of this server
    serverDescription = "The WorldIRC Services Host"
    
    # Please enter the numeric of this server
    numericID = 1
    
    # Please enter the name of the person who administers this server
    adminNick = "laser"
    
    # Please enter their e-mail address
    contactEmail = "chris@worldirc.org"
    
    # Please enter the mask your users use when they are hidden
    hiddenUserMask = ".users.worldirc.org"

import irc.state
state = irc.state.state(WISHConfig())

# Define any upstreams below as so

import p10.connection
upstreams = [
                p10.connection.connection(state).start((HOSTNAME, PORT), PASSWORD)
            ]

# Define any additional modules below as so
import irc.admin
import irc.info
import irc.lusers
import irc.motd
import irc.names
import irc.version
modules =   [
                irc.admin.admin(state),
                irc.info.info(state),
                irc.lusers.lusers(state),
                irc.motd.motd(state),
                irc.names.names(state),
                irc.version.version(state)
            ]

# Execute!
import asyncore
while len(upstreams) > 0:
    asyncore.loop()
    for upstream in upstreams:
        if upstream.connstate == p10.connection.connection.COMPLETE:
            upstreams.remove(upstream)
        else:
            upstream.do_ping()