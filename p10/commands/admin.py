#!/usr/bin/env python

import p10.base64
import genericcommand

class admin(genericcommand.genericcommand):
    """ Returns information about the server """
    
    def handle(self, origin, args):
        self._state.requestAdminInfo(origin, p10.base64.parseNumeric(args[0], self._state.maxClientNumerics))