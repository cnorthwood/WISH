#!/usr/bin/env python

import p10.base64
import genericcommand

class links(genericcommand.genericcommand):
    """ Returns link information about the server """
    
    def handle(self, origin, args):
        self._state.requestLinks(origin, p10.base64.parseNumeric(args[0], self._state.maxClientNumerics), args[1])