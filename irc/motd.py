#!/usr/bin/env python

class motd:
    
    _state = None
    
    def __init__(self, state):
        self._state = state
        state.registerCallback(state.CALLBACK_REQUESTMOTD, self.callbackMOTD)
    
    def callbackMOTD(self, (numeric, target)):
        if target[0] == self._state.getServerID():
            self._state.oobmsg((self._state.getServerID(), None), numeric, "375", [self._state.getServerName() + " Message of the Day"])
            self._state.oobmsg((self._state.getServerID(), None), numeric, "376", ["End of /MOTD."])