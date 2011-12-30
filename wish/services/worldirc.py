#!/usr/bin/env python

class WBot():
    
    _state = None
    
    def __init__(self, state):
        self._state = state
        self._state.new_user(
            (self._state.server_id, None),
            (self._state.server_id, 1),
            "W", "wish", "worldirc.org",
            [('+k', None)], 0, 0, 0, "The WorldIRC Test Bot"
        )
        
        self._state.create_channel(
            (self._state.server_id, 1),
            "#help",
            self._state.ts
        )
        
        self._state.create_channel(
            (self._state.server_id, 1),
            "#opers", self._state.ts
        )
        
        self._state.register_callback(self._state.CALLBACK_CHANNELJOIN,
                                      self.callback_channel_join)
    
    def callback_channel_join(self, origin, name, ts):
        if name in ["#help", "#opers"]:
            self._state.privmsg(
                (self._state.server_id, 1),
                name,
                "Hello, I am the test bot for the next-generation WorldIRC services."
            )
