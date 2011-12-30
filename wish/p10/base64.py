"""
WISH - the WorldIRC Service Host

Utilities for converting base 64 to and from integers

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

# A mapping of base 64 characters to the relevant values
_MAP = {
    "A": 0,
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
    "]": 63
}

_REVMAP = dict(zip(_MAP.values(), _MAP.keys()))

def to_int(chars):
    """
    Convert a base 64 string to its appropriate base-10 integer
    """
    accum = 0
    chars = list(chars)
    chars.reverse()
    chars = ''.join(chars)
    power = 0
    for char in chars:
        try:
            accum = accum + (_MAP[char] * (64 ** power))
        except KeyError:
            raise Base64Error('Invalid base64 character encountered', chars)
        power = power + 1
    return accum


def to_base64(num, pad):
    """
    Convert a base-10 integer to a base-64 string
    """
    # Build a list of all the appropriate characters
    parts = list()
    power = 0
    while num > (64 ** power):
        power = power + 1
    while power >= 0:
        part = num / (64 ** power)
        parts.append(_REVMAP[part])
        num = num - (part * (64 ** power))
        power = power - 1
    parts = ''.join(parts)
    if len(parts) > 1:
        # Trim the valueless characters off the front, apart from if the value
        # is a literal 0
        parts = parts.lstrip('A')
    
    # Do padding
    while len(parts) < pad:
        parts = 'A' + parts
    
    return parts


def parse_numeric(numeric, maxclient):
    """
    Take a numeric and return a tuple of integers, the first representing the
    server numeric, the second the client numeric.
    If the numeric is server-only, then the second element in the pair is set to
    None
    The maxclient is used to return unique numerics
    """
    
    # Short and extended server only numerics
    if len(numeric) == 1 or len(numeric) == 2:
        return (to_int(numeric), None)
    # Short server/client numerics
    elif len(numeric) == 3:
        server = to_int(numeric[0])
        return (server, to_int(numeric[1:3]) & maxclient[server])
    # Universal IRCU server/client numerics
    elif len(numeric) == 4:
        server = to_int(numeric[0])
        return (server, to_int(numeric[1:4]) & maxclient[server])
    # Extended server/client numerics
    elif len(numeric) == 5:
        server = to_int(numeric[0:2])
        return (server, to_int(numeric[2:5]) & maxclient[server])
    else:
        raise Base64Error("Bad length for numeric", numeric)


def create_numeric((server, client)):
    """
    Create a numeric from a pair of integers - with the first representing the
    server numeric, the second the client.
    This only generates extended (5 character) numerics for maximum
    compatibility
    """
    
    # Generate the server half
    servernum = to_base64(server, 2)
    
    # Handle server-only numerics
    clientnum = ""
    if client != None:
        # Generate client half
        clientnum = to_base64(client, 3)
    
    return servernum + clientnum


class Base64Error(Exception):
    """
    An exception that is raised if there is an error generating or parsing the
    base 64
    """
    
    numeric = ""
    
    def __init__(self, value, numeric):
        self.value = value
        self.numeric = numeric
    
    def __str__(self):
        return repr(self.value) + " with numeric " + self.numeric
