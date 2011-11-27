#!/usr/bin/env python

import genericcommand

class squit(genericcommand.genericcommand):
    
    def handle(self, origin, args):
        self._state.quitServer(origin, self._state.nick2numeric(args[0]), args[-1], int(args[1]))