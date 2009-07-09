#!/usr/bin/env python

class parser():
    
    _handlers = dict()
    
    def registerHandler(self, token, handler):
        self._handlers[token] = handler
    
    def parse(self, string):
        
        # The standard requires we only accept strings ending in \r\n or \n
        if (string[-1] != "\n"):
            raise ParseError('Line endings were not as expected', string)
        
        if (len(string)) > 512:
            raise ParseError('Line too long to be valid', string)
        string = string.rstrip()
        
        high_level_parts = string.split(None, 2)
        origin = high_level_parts[0]
        command = high_level_parts[1]
        if not command.isupper():
            raise ParseError('Command not in uppercase', string)
        params = high_level_parts[2]
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
        self._handlers[command].handle(origin, params)

class ParseError(Exception):
    
    line = ""
    
    def __init__(self, value, line):
        self.value = value
        self.line = line
    
    def __str__(self):
        return repr(self.value) + " on line " + self.line
