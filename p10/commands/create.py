#!/usr/bin/env python

import genericcommand

class create(genericcommand.genericcommand):
    """ Handles channel create commands """
    
    def handle(self, origin, args):
        for channel in args[0].split(','):
            # If we return false, we propogate this as a join and bounce a deop
            if not self._state.createChannel(origin, channel, args[1]):
                self._state.joinChannel(origin, channel, ["o"])
                self._state.deop((self._state.getServerID, None), channel, origin)