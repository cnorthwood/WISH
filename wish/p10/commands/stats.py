#!/usr/bin/env python

import genericcommand
import p10.base64

class stats(genericcommand.genericcommand):
    
    def handle(self, origin, args):
        if len(args) > 2:
            extra = args[2]
        else:
            extra = None
        self._state.requestStats(origin, p10.base64.parseNumeric(args[1], self._state.maxClientNumerics), args[0], extra)