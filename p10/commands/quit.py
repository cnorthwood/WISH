#!/usr/bin/env python

import genericcommand

class quit(genericcommand.genericcommand):
    
    def handle(self, origin, args):
        self._state.quit(origin, args[-1])