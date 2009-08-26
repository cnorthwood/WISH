#!/usr/bin/env python

import genericcommand

class wallusers(genericcommand.genericcommand):
    
    def handle(self, origin, args):
        self._state.wallusers(origin, args[-1])