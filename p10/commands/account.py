#!/usr/bin/env python

import p10.parser
import p10.base64
import genericcommand

class account(genericcommand.genericcommand):
    """ Parses the AC/ACCOUNT token - users authenticating """
    
    def handle(self, origin, line):
        self._state.authenticate(origin, p10.base64.parseNumeric(line[0], self._state.maxClientNumerics), line[1])