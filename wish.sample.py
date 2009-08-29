#!/usr/bin/env python

import irc.state
import p10.connection
import asyncore

#
# WISH
# WorldIRC Service Host
#

class WISHConfig:
    
    # Please set the name of this server here
    serverName = "beta.worldirc.org"
    
    # Please enter the numeric of this server
    numericID = 1
    
    # Please enter the name of the person who administers this server
    adminNick = "laser"
    
    # Please enter their e-mail address
    contactEmail = "chris@worldirc.org"
    
    # Please enter the mask your users use when they are hidden
    hiddenUserMask = ".users.worldirc.org"

state = irc.state.state(WISHConfig())

# Define any upstreams below as so

upstreams = [
                p10.connection.connection(state).start((HOSTNAME, PORT), PASSWORD)
            ]

# Execute!
while len(upstreams) > 0:
    asyncore.loop()
    for upstream in upstreams:
        if upstream.connstate == p10.connection.connection.COMPLETE:
            upstreams.remove(upstream)
        else:
            upstream.do_ping()