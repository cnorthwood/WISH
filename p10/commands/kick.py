#!/usr/bin/env python

import genericcommand
import p10.base64

class kick(genericcommand.genericcommand):
    
    def handle(self, origin, args):
        self._state.kick(origin, args[0], p10.base64.parseNumeric(args[1], self._state.maxClientNumerics), args[-1])