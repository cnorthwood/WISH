#!/usr/bin/env python

class lusers:
    
    _state = None
    
    def __init__(self, state):
        self._state = state
        state.registerCallback(state.CALLBACK_REQUESTLUSERS, self.callbackLusers)
    
    def callbackLusers(self, (origin, target, dummy)):
        if target[0] == self._state.getServerID():
            infostr = "There "
            if len(self._state.users) == 1:
                infostr += "is 1 user on "
            else:
                infostr += "are " + str(len(self._state.users)) + " users on "
            if len(self._state.servers) == 1:
                infostr += "1 server."
            else:
                infostr += str(len(self._state.servers)) + " servers."
            self._state.oobmsg((self._state.getServerID(), None), origin, "251", [infostr])
            
            operators = 0
            for user in self._state.users:
                if self._state.users[user].hasMode("o"):
                    operators += 1
            if operators == 1:
                infostr = "operator online."
            else:
                infostr = "operators online."
            self._state.oobmsg((self._state.getServerID(), None), origin, "252", [str(operators), infostr])
            
            if len(self._state.channels) == 1:
                infostr = "channel formed."
            else:
                infostr = "channels formed."
            self._state.oobmsg((self._state.getServerID(), None), origin, "254", [str(len(self._state.channels)), infostr])
            
            local = 0
            for user in self._state.users:
                if user[0] == self._state.getServerID():
                    local += 1
            infostr = "I have "
            if local == 1:
                infostr += "1 client and "
            else:
                infostr += str(local) + " clients and "
            if len(self._state.servers[self._state.getServerID()].children) == 1:
                infostr += "1 server."
            else:
                infostr += str(len(self._state.servers[self._state.getServerID()].children)) + " servers."
            self._state.oobmsg((self._state.getServerID(), None), origin, "255", [infostr])