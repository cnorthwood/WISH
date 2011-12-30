"""
WISH - the WorldIRC Service Host

Responding to admin requests

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

class AdminResponder():
    """
    An class for handling requests for information about the administrators of
    this server
    """
    
    def __init__(self, state):
        self._state = state
        state.register_callback(state.CALLBACK_REQUESTADMIN,
                               self.callback_admininfo)
    
    def callback_admininfo(self, origin, target):
        """
        Send information about the admins for this server back to a requesting
        user, when this server is the target
        """
        
        if target[0] == self._state.server_id:
            self._state.oobmsg(
                (self._state.server_id, None),
                origin,
                "256",
                ["Administrative info about " + self._state.server_name]
            )
            
            self._state.oobmsg(
                (self._state.server_id, None),
                origin,
                "257",
                [self._state.server_description]
            )
            
            self._state.oobmsg(
                (self._state.server_id, None),
                origin,
                "258",
                ["Administrator is " + self._state.admin_name]
            )
            
            self._state.oobmsg(
                (self._state.server_id, None),
                origin,
                "259",
                [self._state.contact_email]
            )
