#!/usr/bin/env python

import genericcommand

class wallops(genericcommand.genericcommand):
    
    def handle(self, origin, args):
        self._state.wallops(origin, args[-1])