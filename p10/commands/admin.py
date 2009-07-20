#!/usr/bin/env python

import p10.base64
import genericcommand

class admin(genericcommand.genericcommand):
    """ Returns the administrative information for the server """
    
    def handle(self, origin, args):
        if p10.base64.parseNumeric(args[0]) == (self._state.getServerID(), None):
            self._state.sendLine(None, "256", [p10.base64.createNumeric(origin), "Administrative information about " + self._state.getServerName()])
            self._state.sendLine(None, "257", [p10.base64.createNumeric(origin), "This is WISH for " + self._state.getNetworkName()])
            self._state.sendLine(None, "258", [p10.base64.createNumeric(origin), "The nominated administrative contact is " + self._state.getAdminNick()])
            self._state.sendLine(None, "259", [p10.base64.createNumeric(origin), "E-mail queries about this server should be directed to " + self._state.getContactEmail()])

class num256(genericcommand.genericcommand):
    pass

class num257(genericcommand.genericcommand):
    pass

class num258(genericcommand.genericcommand):
    pass

class num259(genericcommand.genericcommand):
    pass