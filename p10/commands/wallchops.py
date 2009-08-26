#!/usr/bin/env python

import genericcommand

class wallchops(genericcommand.genericcommand):
    
    def handle(self, origin, args):
        self._state.wallchops(origin, args[0], args[-1])