#!/usr/bin/env python

import genericcommand
import p10.base64

class pong(genericcommand.genericcommand):
    """ Parses servers being introduced """
    
    _connection = None
    
    def __init__(self, state, connection):
        self._connection = connection
        genericcommand.genericcommand.__init__(self, state)
    
    def handle(self, origin, args):
        self._connection.registerPong()