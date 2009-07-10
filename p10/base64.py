#!/usr/bin/env python

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

def toint(chars):
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

def tobase64(num):
    parts = list()
    power = 0
    while num > (64 ** power):
        power = power + 1
    print
    while power >= 0:
        part = num / (64 ** power)
        parts.append(_revmap[part])
        num = num - (part * (64 ** power))
        power = power - 1
    parts = ''.join(parts)
    if len(parts) > 1:
        return parts.lstrip('A')
    else:
        return parts

def parsenumeric(numeric):
    if len(numeric) == 1 or len(numeric) == 2:
        return (toint(numeric), None)
    elif len(numeric) == 3:
        return (toint(numeric[0]), toint(numeric[1:3]))
    elif len(numeric) == 4:
        return (toint(numeric[0]), toint(numeric[1:4]))
    elif len(numeric) == 5:
        return (toint(numeric[0:2]), toint(numeric[2:5]))

# Send only extended numerics for maximum compatibility
def createnumeric((server, client)):
    servernum = tobase64(server)
    while len(servernum) < 2:
        servernum = "A" + servernum
    clientnum = ""
    if client != None:
        clientnum = tobase64(client)
        while len(clientnum) < 3:
            clientnum = "A" + clientnum
    return servernum + clientnum

class Base64Error(Exception):
    
    numeric = ""
    
    def __init__(self, value, numeric):
        self.value = value
        self.numeric = numeric
    
    def __str__(self):
        return repr(self.value) + " with numeric " + self.numeric
