#!/usr/bin/env python

import genericcommand
import p10.base64

class svsjoin(genericcommand.genericcommand):
    
    def handle(self, origin, args):
        target = p10.base64.parseNumeric(args[0], self._state.maxClientNumerics)
        for channel in args[1].split(","):
            self._state.joinChannel(origin, target, channel, [])

#
# Caution!
#
# svsjoin's as defined in Beware's spec have race conditions - the solution is
# the same as for SVSNICK, simply propogate the message to the target and then
# the target server sends a join out as per usual.