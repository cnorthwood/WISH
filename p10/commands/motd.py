#!/usr/bin/env python

import p10.base64
import genericcommand

class motd(genericcommand.genericcommand):
    """ Returns user information about the server """
    
    def handle(self, origin, args):
        self._state.requestMOTD(origin, p10.base64.parseNumeric(args[0], self._state.maxClientNumerics))