#!/usr/bin/env python

import unittest
import p10.commands.topic

class StateDouble:
    insight = []
    def __init__(self):
        self.insight = []
    def changeTopic(self, origin, channel, topic, topic_ts, channel_ts):
        self.insight.append((channel, topic, topic_ts, channel_ts))

class TopicTest(unittest.TestCase):
    
    def testSimpleChange(self):
        s = StateDouble()
        c = p10.commands.topic.topic(s)
        c.handle((1,1), ["#test", "8", "10", "New topic"])
        self.assertEquals([("#test", "New topic", 10, 8)], s.insight)
    
    def testNoTSChange(self):
        s = StateDouble()
        c = p10.commands.topic.topic(s)
        c.handle((1,1), ["#test", "New topic"])
        self.assertEquals([("#test", "New topic", 0, 0)], s.insight)