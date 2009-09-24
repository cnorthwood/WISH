#!/usr/bin/env python

import fnmatch

class links:
    
    _state = None
    
    def __init__(self, state):
        self._state = state
        state.registerCallback(state.CALLBACK_REQUESTLINKS, self.callbackLinks)
    
    def callbackLinks(self, (origin, target, mask)):
        if target[0] == self._state.getServerID():
            for server in self._state.servers:
                if fnmatch.fnmatch(self._state.servers[server].name, mask):
                    upstream = self._state.servers[server].origin
                    if upstream == None:
                        upstream = self._state.getServerName()
                    else:
                        upstream = self._state.numeric2nick((upstream, None))
                    self._state.oobmsg((self._state.getServerID(), None), origin, "364", [self._state.servers[server].name, upstream, str(self._state.servers[server].hops) + " " + self._state.servers[server].protocol + " " + self._state.servers[server].description])
            self._state.oobmsg((self._state.getServerID(), None), origin, "365", [mask, "End of /LINKS list."])