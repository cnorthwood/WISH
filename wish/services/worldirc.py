#!/usr/bin/env python

class worldirc:
    
    _state = None
    
    def __init__(self, state):
        self._state = state
        self._state.newUser((self._state.server_id, None), (self._state.server_id, 1), "W", "wish", "worldirc.org", [('+k', None)], 0, 0, 0, "The WorldIRC Test Bot")
        self._state.createChannel((self._state.server_id, 1), "#help", self._state.ts())
        self._state.createChannel((self._state.server_id, 1), "#opers", self._state.ts())
    
    def callbackChannelCreate(self, (origin, name, ts)):
        self._state.privmsg((self._state.server_id, 1), "#opers", "Hello, I am the test bot for the next-generation WorldIRC services. I just got channel creation info about " + name)
        if name == "#help" or name == "#opers":
            
            self._state.privmsg((self._state.server_id, 1), name, "Hello, I am the test bot for the next-generation WorldIRC services.")