#!/usr/bin/env python

import genericcommand
import p10.base64

class ping(genericcommand.genericcommand):
    """ Parses servers being introduced """
    
    _connection = None
    
    def __init__(self, state, connection):
        self._connection = connection
        genericcommand.genericcommand.__init__(self, state)
    
    def handle(self, origin, args):
        if len(args) == 1:
            self._connection.registerPing(args[0])
        else:
            if args[1] == self._state.numeric2nick((self._state.getServerID(), None)):
                self._connection.registerPing(args[0])
            else:
                self._state.registerPing(origin, args[0], args[1])