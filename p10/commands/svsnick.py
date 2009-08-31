#!/usr/bin/env python

import genericcommand
import p10.base64

class svsnick(genericcommand.genericcommand):
    
    def handle(self, origin, args):
        self._state.changeNick(origin, p10.base64.parseNumeric(args[0], self._state.maxClientNumerics), args[1], self._state.ts())

#
# CAUTION!
#
# Beware's svsnick has a fairly major race condition - N and SN messages
# can cross and there's no way to solve it using the current protocol spec.
#
# The solution is fairly simple, to not actually enact SNs apart from if the
# user is local, and then send an N out as if the user had changed locally.