#!/usr/bin/env python

import p10.base64
import genericcommand

class names(genericcommand.genericcommand):
    """ Returns users on a channel """
    
    def handle(self, origin, args):
        self._state.sendChannelUsers(origin, p10.base64.parseNumeric(args[1], self._state.maxClientNumerics), args[0])