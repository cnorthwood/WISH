#!/usr/bin/env python

class worldirc:
    
    _state = None
    
    def __init__(self, state):
        self._state = state
        self._state.newUser((self._state.getServerID(), None), (self._state.getServerID(), 1), "W", "wish", "worldirc.org", [('+k', None)], 0, 0, 0, "The WorldIRC Test Bot")
        self._state.registerCallback(self._state.CALLBACK_CHANNELCREATE, self.callbackChannelCreate)
    
    def callbackChannelCreate(self, (origin, name, ts)):
        if name == "#help" or name == "#opers":
            self._state.joinChannel((self._state.getServerID(), 1), (self._state.getServerID(), 1), name, "ov", self._state.ts())
            self._state.privmsg((self._state.getServerID(), 1), name, "Hello, I am the test bot for the next-generation WorldIRC services.")