"""
WISH - the WorldIRC Service Host

Responding to requests about local users

Copyright (c) 2009-2011, Chris Northwood
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of Chris Northwood nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

class LusersResponder():
    """
    A class to handle callbacks for requests about local users on this server
    """
    
    def __init__(self, state):
        self._state = state
        state.register_callback(state.CALLBACK_REQUESTLUSERS,
                                self.callback_lusers)
    
    def callback_lusers(self, origin, target, dummy):
        """
        Respond to information about local users when this server is the target
        """
        
        if target[0] == self._state.server_id:
            infostr = "There "
            
            if len(self._state.users) == 1:
                infostr += "is 1 user on "
            else:
                infostr += "are " + str(len(self._state.users)) + " users on "
            
            if len(self._state.servers) == 1:
                infostr += "1 server."
            else:
                infostr += str(len(self._state.servers)) + " servers."
            
            self._state.oobmsg(
                (self._state.server_id, None),
                origin,
                "251",
                [infostr]
            )
            
            operators = 0
            for user in self._state.users:
                if self._state.users[user].has_mode("o"):
                    operators += 1
                
            if operators == 1:
                infostr = "operator online."
            else:
                infostr = "operators online."
            
            self._state.oobmsg(
                (self._state.server_id, None),
                origin,
                "252",
                [
                    str(operators),
                    infostr
                ]
            )
            
            if len(self._state.channels) == 1:
                infostr = "channel formed."
            else:
                infostr = "channels formed."
            
            self._state.oobmsg(
                (self._state.server_id, None),
                origin,
                "254",
                [
                    str(len(self._state.channels)),
                    infostr
                ]
            )
            
            local = 0
            for user in self._state.users:
                if user[0] == self._state.server_id:
                    local += 1
            infostr = "I have "
            
            if local == 1:
                infostr += "1 client and "
            else:
                infostr += str(local) + " clients and "
            
            if len(self._state.servers[self._state.server_id].children) == 1:
                infostr += "1 server."
            else:
                infostr += str(
                    len(self._state.servers[self._state.server_id].children))
                infostr += " servers."
            
            self._state.oobmsg(
                (self._state.server_id, None),
                origin,
                "255",
                [infostr]
            )
