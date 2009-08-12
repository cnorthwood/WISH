#!/usr/bin/env python

import genericcommand

class topic(genericcommand.genericcommand):
    
    def handle(self, origin, args):
        channel = args[0]
        newtopic = args[-1]
        if len(args) > 2:
            topic_ts = int(args[-2])
        else:
            topic_ts = 0
        if len(args) > 3:
            channel_ts = int(args[-3])
        else:
            channel_ts = 0
        self._state.changeTopic(origin, channel, newtopic, topic_ts, channel_ts)