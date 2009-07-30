#!/usr/bin/env python

import genericcommand

class invite(genericcommand.genericcommand):
    
    def handle(self, origin, args):
        target = self._state.nick2numeric(args[0])
        channel = args[1]
        self._state.invite(origin, target, channel)