#!/usr/bin/env python

import genericcommand
import p10.base64

class numberrelay(genericcommand.genericcommand):
    
    _connection = None
    
    def __init__(self, state, number):
        self._number = number
        genericcommand.genericcommand.__init__(self, state)
    
    def handle(self, origin, args):
        self._state.oobmsg(origin, self._number, args)