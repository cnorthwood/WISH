#!/usr/bin/env python

import genericcommand
import p10.base64

class pong(genericcommand.genericcommand):
    
    _connection = None
    
    def __init__(self, state, connection):
        self._connection = connection
        genericcommand.genericcommand.__init__(self, state)
    
    def handle(self, origin, args):
        if p10.base64.parseNumeric(args[1], self._state.maxClientNumerics) == (self._state.getServerID(), None):
            self._connection.registerPong()
        else:
            self._state.registerPong(origin, args[0], args[1])