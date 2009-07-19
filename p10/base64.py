#!/usr/bin/env python

""" A mapping of base 64 characters to the relevant values """
_map = {"A": 0,
        "B": 1,
        "C": 2,
        "D": 3,
        "E": 4,
        "F": 5,
        "G": 6,
        "H": 7,
        "I": 8,
        "J": 9,
        "K": 10,
        "L": 11,
        "M": 12,
        "N": 13,
        "O": 14,
        "P": 15,
        "Q": 16,
        "R": 17,
        "S": 18,
        "T": 19,
        "U": 20,
        "V": 21,
        "W": 22,
        "X": 23,
        "Y": 24,
        "Z": 25,
        "a": 26,
        "b": 27,
        "c": 28,
        "d": 29,
        "e": 30,
        "f": 31,
        "g": 32,
        "h": 33,
        "i": 34,
        "j": 35,
        "k": 36,
        "l": 37,
        "m": 38,
        "n": 39,
        "o": 40,
        "p": 41,
        "q": 42,
        "r": 43,
        "s": 44,
        "t": 45,
        "u": 46,
        "v": 47,
        "w": 48,
        "x": 49,
        "y": 50,
        "z": 51,
        "0": 52,
        "1": 53,
        "2": 54,
        "3": 55,
        "4": 56,
        "5": 57,
        "6": 58,
        "7": 59,
        "8": 60,
        "9": 61,
        "[": 62,
        "]": 63}

_revmap = dict(zip(_map.values(), _map.keys()))

def toInt(chars):
    """ Convert a base 64 string to its appropriate base-10 integer """
    accum = 0
    chars = list(chars)
    chars.reverse()
    chars = ''.join(chars)
    power = 0
    for char in chars:
        try:
            accum = accum + (_map[char] * (64 ** power))
        except KeyError:
            raise Base64Error('Invalid base64 character encountered', chars)
        power = power + 1
    return accum

def toBase64(num):
    """ Convert a base-10 integer to a base-64 string """
    # Build a list of all the appropriate characters
    parts = list()
    power = 0
    while num > (64 ** power):
        power = power + 1
    while power >= 0:
        part = num / (64 ** power)
        parts.append(_revmap[part])
        num = num - (part * (64 ** power))
        power = power - 1
    parts = ''.join(parts)
    if len(parts) > 1:
        # Trim the valueless characters off the front, apart from if the value is a literal 0
        return parts.lstrip('A')
    else:
        return parts

def parseNumeric(numeric):
    """ Take a numeric and return a tuple of integers, the first representing the server numeric, the second the client numeric.
        If the numeric is server-only, then the second element in the pair is set to None """
    
    # Short and extended server only numerics
    if len(numeric) == 1 or len(numeric) == 2:
        return (toInt(numeric), None)
    # Short server/client numerics
    elif len(numeric) == 3:
        return (toInt(numeric[0]), toInt(numeric[1:3]))
    # Universal IRCU server/client numerics
    elif len(numeric) == 4:
        return (toInt(numeric[0]), toInt(numeric[1:4]))
    # Extended server/client numerics
    elif len(numeric) == 5:
        return (toInt(numeric[0:2]), toInt(numeric[2:5]))

def createNumeric((server, client)):
    """ Create a numeric from a pair of integers - with the first representing the server numeric, the second the client.
        This only generates extended (5 character) numerics for maximum compatibility """
    
    # Generate the server half
    servernum = toBase64(server)
    
    # Pad to required length
    while len(servernum) < 2:
        servernum = "A" + servernum
    
    # Handle server-only numerics
    clientnum = ""
    if client != None:
        # Generate client half
        clientnum = toBase64(client)
        
        # Pad to correct length
        while len(clientnum) < 3:
            clientnum = "A" + clientnum
    
    return servernum + clientnum

class Base64Error(Exception):
    """ An exception that is raised if there is an error generating or parsing the base 64 """
    
    numeric = ""
    
    def __init__(self, value, numeric):
        self.value = value
        self.numeric = numeric
    
    def __str__(self):
        return repr(self.value) + " with numeric " + self.numeric
