#!/usr/bin/env python

class genericcommand:
    
    _state = None
    
    def __init__(self, state):
        self._state = state
    
    def handle(self, origin, line):
        pass