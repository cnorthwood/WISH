#!/usr/bin/env python

import genericcommand
import p10.base64

class svsnick(genericcommand.genericcommand):
    
    def handle(self, origin, args):
        self._state.changeNick(origin, p10.base64.parseNumeric(args[0], self._state.maxClientNumerics), args[1], self._state.ts())

