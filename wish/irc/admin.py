#!/usr/bin/env python

class admin:
    
    _state = None
    
    def __init__(self, state):
        self._state = state
        state.registerCallback(state.CALLBACK_REQUESTADMIN, self.callbackAdminInfo)
    
    def callbackAdminInfo(self, (origin, target)):
        if target[0] == self._state.getServerID():
            self._state.oobmsg((self._state.getServerID(), None), origin, "256", ["Administrative info about " + self._state.getServerName()])
            self._state.oobmsg((self._state.getServerID(), None), origin, "257", [self._state.getServerDescription()])
            self._state.oobmsg((self._state.getServerID(), None), origin, "258", ["Administrator is " + self._state.getAdminName()])
            self._state.oobmsg((self._state.getServerID(), None), origin, "259", [self._state.getContactEmail()])