#!/usr/bin/env python

import genericcommand
import p10.base64

class kill(genericcommand.genericcommand):
    
    def handle(self, origin, args):
        target = args[0]
        info = args[1].split(None, 1)
        path = info[0].split("!")
        reason = info[1].strip("()")
        self._state.kill(origin, p10.base64.parseNumeric(target, self._state.maxClientNumerics), path, reason)