#!/usr/bin/env python

from wish.p10.commands.basecommand import BaseCommand

class ClearModeHandler(BaseCommand):
    
    def handle(self, origin, args):
        modes = []
        for mode in args[1]:
            if mode == "b":
                self._state.clear_channel_bans(origin, args[0])
            elif mode == "o":
                self._state.clear_channel_ops(origin, args[0])
            elif mode == "v":
                self._state.clear_channel_voices(origin, args[0])
            else:
                modes.append(('-' + mode, None))
        if len(modes) > 0:
            self._state.change_channel_mode(origin, args[0], modes)
