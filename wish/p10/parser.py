"""
WISH - the WorldIRC Service Host

Classes for parsing P10

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

from wish.p10.base64 import parse_numeric, create_numeric

class Parser():
    """
    Takes a raw line from the connection, tokenises it and then passes it on
    to an appropriate handler
    """
    
    def __init__(self, maxclientnum):
        self._handlers = dict()
        self._maxclientnum = maxclientnum
    
    def register_handler(self, token, handler):
        """
        Add a new handler for a particular token
        """
        self._handlers[token] = handler
    
    def _pass_to_handler(self, origin, token, args):
        """
        Pass something parsed to the appropriate handler
        """
        try:
            self._handlers[token].handle(origin, args)
        except KeyError:
            raise ParseError("Unknown command", None)
    
    def _check_line_is_good(self, string):
        """
        Check the raw line meets our various standards, tidy it up and return it
        """
        # The standard requires we only accept strings ending in \r\n or \n
        if (string[-1] != "\n"):
            raise ParseError('Line endings were not as expected', string)
        
        # The standard places a limit on line lengths
        if (len(string)) > 512:
            raise ProtocolError('Line too long to be valid', string)
        
        # Trim our trailing whitespace/line endings
        return string.rstrip()
    
    def _parse_params(self, params):
        """
        Further break up our body into individual parameters
        """
        if params[0] == ":":
            params = [params[1:]]
        else:
            params = params.split(" :", 1)
            if len(params) == 1:
                last_arg = None
            else:
                last_arg = params[1]
            params = params[0].split(None)
            if last_arg != None:
                params.append(last_arg)
        return params
    
    def parse_pre_auth(self, string, origin):
        """
        Parse strings before authentication is established
        """
        # Tidy up our line
        string = self._check_line_is_good(string)
        
        # Break up into token and body
        high_level_parts = string.split(None, 1)
        command = high_level_parts[0]
        if not command.isupper() and not command.isdigit():
            raise ProtocolError('Command not in uppercase', string)
        params = self._parse_params(high_level_parts[1])
        
        # If this is an invalid command, pass it upwards
        try:
            self._pass_to_handler(origin, command, params)
        except ParseError, error:
            raise ParseError(error.value, string)
    
    def parse(self, string):
        """
        Take a string, parse it into our internal form and pass it on
        """
        # Tidy up our line
        string = self._check_line_is_good(string)
        
        # Break up into origin, token and body
        high_level_parts = string.split(None, 2)
        origin = parse_numeric(high_level_parts[0], self._maxclientnum)
        command = high_level_parts[1]
        if not command.isupper() and not command.isdigit():
            raise ProtocolError('Command not in uppercase', string)
        if len(high_level_parts) > 2:
            params = self._parse_params(high_level_parts[2])
        else:
            params = []
        
        # If this is an invalid command, pass it upwards
        try:
            self._pass_to_handler(origin, command, params)
        except ParseError, error:
            raise ParseError(error.value, string)
    
    def build(self, origin, token, args):
        """
        Build a string suitable for sending
        """
        # If the last argument is "long", package it for sending
        if len(args) > 0:
            if args[-1].find(" ") > -1:
                build_last_arg = ":" + args[-1]
                build_args = args[0:-1] + build_last_arg.split(" ")
            else:
                build_args = args
        else:
            build_args = []
        # Build the line
        # Future compatibility - only send \n
        ret = create_numeric(origin) + " " + token + " " \
            + " ".join(build_args) + "\n"
        
        # Check we're not sending things which are protocol violations
        if len(ret) > 512:
            raise ProtocolError('Line too long to send')
        if not token.isupper() and not token.isdigit():
            raise ProtocolError('Command not in uppercase during build')
        
        return ret


class ParseError(Exception):
    """ An exception thrown if a line can not be parsed """
    
    def __init__(self, value, line):
        self.value = value
        self.line = line
    
    def __str__(self):
        return repr(self.value) + " on line " + self.line


class ProtocolError(Exception):
    """ An exception if a line is a protocol violation """
    pass
