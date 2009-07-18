#!/usr/bin/env python

import p10.parser
import p10.base64

class account:
    
    _state = None
    
    def __init__(self, state):
        self._state = state
    
    def handle(self, origin, line):
        # Only accept from servers
        if (origin[1] != None):
            raise p10.parser.ProtocolError("ACCOUNT token received from non-server")
        
        self._state.authenticate(p10.base64.parseNumeric(line[0]), line[1])