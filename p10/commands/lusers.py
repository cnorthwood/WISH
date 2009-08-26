#!/usr/bin/env python

import p10.base64
import genericcommand

class lusers(genericcommand.genericcommand):
    """ Returns user information about the server """
    
    def handle(self, origin, args):
        self._state.requestLusers(origin, p10.base64.parseNumeric(args[1], self._state.maxClientNumerics), args[0])