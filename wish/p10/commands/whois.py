#!/usr/bin/env python

import genericcommand
import p10.base64

class whois(genericcommand.genericcommand):
    
    def handle(self, origin, args):
        for search in args[1].split(","):
            self._state.requestWhois(origin, p10.base64.parseNumeric(args[0], self._state.maxClientNumerics), search)