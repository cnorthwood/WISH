#!/usr/bin/env python

import genericcommand
import p10.base64

class svsjoin(genericcommand.genericcommand):
    
    def handle(self, origin, args):
        target = p10.base64.parseNumeric(args[0], self._state.maxClientNumerics)
        for channel in args[1].split(","):
            self._state.joinChannel(origin, target, channel, [])