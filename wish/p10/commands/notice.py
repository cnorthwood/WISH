#!/usr/bin/env python

import genericcommand
import p10.base64

class notice(genericcommand.genericcommand):
    
    def handle(self, origin, args):
        try:
            target = p10.base64.parseNumeric(args[0], self._state.maxClientNumerics)
        except p10.base64.Base64Error:
            target = args[0]
        self._state.notice(origin, target, args[-1])