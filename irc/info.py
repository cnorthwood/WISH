#!/usr/bin/env python

class info:
    
    _state = None
    
    def __init__(self, state):
        self._state = state
        state.registerCallback(state.CALLBACK_REQUESTINFO, self.callbackInfoRequest)
    
    def callbackInfoRequest(self, (origin, target)):
        if target[0] == self._state.getServerID():
            infostr = "I know "
            if len(self._state.servers) == 1:
                infostr += "1 server and "
            else:
                infostr += str(len(self._state.servers)) + " servers and "
            if len(self._state.users) == 1:
                infostr += "1 user on "
            else:
                infostr += str(len(self._state.users)) + " users on "
            if len(self._state.channels) == 1:
                infostr += "1 channel."
            else:
                infostr += str(len(self._state.channels)) + " channels."
            self._state.oobmsg((self._state.getServerID(), None), "371", origin, [infostr])
            self._state.oobmsg((self._state.getServerID(), None), "374", origin, ["End of /INFO list"])