#!/usr/bin/env python

import genericcommand

class wallvoices(genericcommand.genericcommand):
    
    def handle(self, origin, args):
        self._state.wallvoices(origin, args[0], args[-1])