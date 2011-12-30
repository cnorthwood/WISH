"""
WISH - the WorldIRC Service Host

Handling requests for names

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

class NamesResponder():
    """
    Handles callbacks for people requesting names of people on channel from the
    point of view of this server
    """
    
    def __init__(self, state):
        self._state = state
        state.register_callback(state.CALLBACK_REQUESTNAMES, self.callback_names)
    
    def callback_names(self, origin, target, channels):
        """
        Respond to requests for a list of names of who's on each channel
        """
        
        if target[0] == self._state.server_id:
            
            for channel in channels:
                
                # Decorate response based on user's current statuc
                if self._state.channels[channel].isop(origin):
                    rstate = "@"
                else:
                    rstate = "="
                
                names = ""
                for user in self._state.channels[channel].users:
                    
                    # Decorate status of each current user
                    prefix = ""
                    if self._state.channels[channel].isop(user):
                        prefix = "@"
                    elif self._state.channels[channel].isvoice(user):
                        prefix = "+"
                    names += prefix + self._state.numeric2nick(user) + " "
                
                self._state.oobmsg(
                    (self._state.server_id, None),
                    origin,
                    "353",
                    [rstate, channel, names.strip()]
                )
            
            self._state.oobmsg(
                (self._state.server_id, None),
                origin,
                "366", [",".join(channels), "End of /NAMES list."]
            )
