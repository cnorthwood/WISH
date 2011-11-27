#!/usr/bin/env python

import genericcommand
import p10.base64

class time(genericcommand.genericcommand):
    
    def handle(self, origin, args):
        self._state.requestTime(origin, p10.base64.parseNumeric(args[0], self._state.maxClientNumerics))