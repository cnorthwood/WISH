#!/usr/bin/env python

class names:
    
    _state = None
    
    def __init__(self, state):
        self._state = state
        state.registerCallback(state.CALLBACK_REQUESTNAMES, self.callbackNames)
    
    def callbackNames(self, (origin, target, channels)):
        if target[0] == self._state.getServerID():
            for channel in channels:
                if self._state.channels[channel].isop(origin):
                    rstate = "@"
                else:
                    rstate = "="
                names = ""
                for user in self._state.channels[channel].users():
                    prefix = ""
                    if self._state.channels[channel].isop(user):
                        prefix = "@"
                    elif self._state.channels[channel].isvoice(user):
                        prefix = "+"
                    names += prefix + self._state.numeric2nick(user) + " "
                self._state.oobmsg((self._state.getServerID(), None), origin, "353", [rstate, channel, names.strip()])
            self._state.oobmsg((self._state.getServerID(), None), origin, "366", [",".join(channels), "End of /NAMES list."])