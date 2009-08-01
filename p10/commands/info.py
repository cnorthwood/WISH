#!/usr/bin/env python

import sys
import p10.base64
import genericcommand

class info(genericcommand.genericcommand):
    """ Returns information about the server """
    
    def handle(self, origin, args):
        self._state.sendServerInfo(origin, p10.base64.parseNumeric(args[0], self._state.maxClientNumerics))