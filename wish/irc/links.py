"""
WISH - the WorldIRC Service Host

Responding to requests about links

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

import fnmatch

class LinksResponder():
    """
    Handles callbacks for remote links requests
    """
    
    def __init__(self, state):
        self._state = state
        state.register_callback(state.CALLBACK_REQUESTLINKS,
                               self.callback_links)
    
    def callback_links(self, origin, target, mask):
        """
        Sends a message back to the origin about the links from this server
        """
        
        if target[0] == self._state.server_id:
            for server in self._state.servers:
                
                # Check that the upstream server matches the mask
                if fnmatch.fnmatch(self._state.servers[server].name, mask):
                    upstream = self._state.servers[server].origin
                    if upstream == None:
                        upstream = self._state.server_name
                    else:
                        upstream = self._state.numeric2nick((upstream, None))
                        
                    self._state.oobmsg(
                        (self._state.server_id, None),
                        origin,
                        "364",
                        [
                            self._state.servers[server].name,
                            upstream,
                            str(self._state.servers[server].hops)
                            + " "
                            + self._state.servers[server].protocol
                            + " "
                            + self._state.servers[server].description
                        ]
                    )
            
            self._state.oobmsg(
                (self._state.server_id, None),
                origin,
                "365",
                [mask, "End of /LINKS list."]
            )
