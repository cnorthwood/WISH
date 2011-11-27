#!/usr/bin/env python

class version:
    
    _state = None
    
    def __init__(self, state):
        self._state = state
        state.registerCallback(state.CALLBACK_REQUESTVERSION, self.callbackRequestVersion)
    
    def callbackRequestVersion(self, (origin, target)):
        if target[0] == self._state.getServerID():
            self._state.oobmsg((self._state.getServerID(), None), origin, "351", ["The WorldIRC Service Host - http://www.pling.org.uk/projects/wish/"])