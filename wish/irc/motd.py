"""
WISH - the WorldIRC Service Host

Responding to requests for the Message Of The Day

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

class MotdResponder():
    """
    Handles callbacks for messages of the day for this server
    """
    
    def __init__(self, state):
        self._state = state
        state.register_callback(state.CALLBACK_REQUESTMOTD, self.callback_motd)
    
    def callback_motd(self, numeric, target):
        """
        Sends an MOTD back to the origin numeric for this server
        """
        
        if target[0] == self._state.server_id:
            self._state.oobmsg(
                (self._state.server_id, None),
                numeric,
                "375",
                [self._state.server_name + " Message of the Day"]
            )
            
            self._state.oobmsg(
                (self._state.server_id, None),
                numeric,
                "376",
                ["End of /MOTD."]
            )
