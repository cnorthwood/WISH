#!/usr/bin/env python

class BaseCommand(object):
    
    def __init__(self, state):
        self._state = state
    
    def handle(self, origin, line):
        pass
