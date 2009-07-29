#!/usr/bin/env python

import sys
import p10.base64
import genericcommand

class info(genericcommand.genericcommand):
    """ Returns information about the server """
    
    def handle(self, origin, args):
        if p10.base64.parseNumeric(args[0]) == (self._state.getServerID(), None):
            self._state.sendLine(None, "371", [p10.base64.createNumeric(origin), "Python " + sys.version + " on " + sys.platform])
            self._state.sendLine(None, "374", [p10.base64.createNumeric(origin), "End of INFO"])