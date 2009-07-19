#!/usr/bin/env python

import base64

class parser:
    """ Takes a raw line from the connection, tokenises it and then passes it on to an appropriate handler """
    
    _handlers = dict()
    
    def __init__(self):
        self._handlers = dict()
    
    def registerHandler(self, token, handler):
        """ Add a new handler for a particular token """
        self._handlers[token] = handler
    
    def _passToHandler(self, origin, token, args):
        """ Pass something parsed to the appropriate handler """
        try:
            self._handlers[token].handle(origin, args)
        except KeyError:
            raise ParseError("Unknown command", None)
    
    def parse(self, string):
        """ Take a string, parse it into our internal form and pass it on """
        
        # The standard requires we only accept strings ending in \r\n or \n
        if (string[-1] != "\n"):
            raise ParseError('Line endings were not as expected', string)
        
        # The standard places a limit on line lengths
        if (len(string)) > 512:
            raise ProtocolError('Line too long to be valid', string)
        
        # Trim our trailing whitespace/line endings
        string = string.rstrip()
        
        # Break up into origin, token and body
        high_level_parts = string.split(None, 2)
        origin = base64.parseNumeric(high_level_parts[0])
        command = high_level_parts[1]
        if not command.isupper():
            raise ProtocolError('Command not in uppercase', string)
        params = high_level_parts[2]
        
        # Further break up our body into individual parameters
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
        
        # If this is an invalid command, pass it upwards
        try:
            self._passToHandler(origin, command, params)
        except ParseError, error:
            raise ParseError(error.value, string)
    
    def build(self, origin, token, args):
        """ Build a string suitable for sending """
        # If the last argument is "long", package it for sending
        if args[-1].find(" ") > -1:
            build_last_arg = ":" + args[-1]
            build_args = args[0:-1] + build_last_arg.split(" ")
        else:
            build_args = args
        # Build the line
        ret = base64.createNumeric(origin) + " " + token + " " + " ".join(build_args) + "\r\n"
        
        # Check we're not sending things which are protocol violations
        if len(ret) > 512:
            raise ProtocolError('Line too long to send', ret)
        if not token.isupper():
            raise ProtocolError('Command not in uppercase during build', ret)
        
        # Pass the line to our handlers to maintain state
        try:
            self._passToHandler(origin, token, args)
        except ParseError, error:
            raise ParseError(error.value, ret)
        
        return ret

class ParseError(Exception):
    """ An exception thrown if a line can not be parsed """
    
    line = ""
    
    def __init__(self, value, line):
        self.value = value
        self.line = line
    
    def __str__(self):
        return repr(self.value) + " on line " + self.line

class ProtocolError(ParseError):
    """ An exception if a line is a protocol violation """
    pass
