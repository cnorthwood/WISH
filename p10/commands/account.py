#!/usr/bin/env python

import p10.parser
import p10.base64

class account:
    """ Parses the AC/ACCOUNT token - users authenticating """
    
    _state = None
    
    def __init__(self, state):
        self._state = state
    
    def handle(self, origin, line):
        # Only accept from servers
        if (origin[1] != None):
            raise p10.parser.ProtocolError("ACCOUNT token received from non-server", " ".join(line))
        
        self._state.authenticate(p10.base64.parseNumeric(line[0]), line[1])