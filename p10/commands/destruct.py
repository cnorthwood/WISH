#!/usr/bin/env python

import genericcommand

class destruct(genericcommand.genericcommand):
    
    def handle(self, origin, args):
        self._state.destroyChannel(origin, args[0], int(args[1]))