#!/usr/bin/env python

import genericcommand
import p10.base64

class privmsg(genericcommand.genericcommand):
    
    def handle(self, origin, args):
        try:
            target = p10.base64.parseNumeric(args[0], self._state.maxClientNumerics)
        except p10.base64.Base64Error:
            target = args[0]
        self._state.privmsg(origin, target, args[-1])