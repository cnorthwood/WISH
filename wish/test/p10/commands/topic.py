#!/usr/bin/env python

import unittest
from wish.p10.commands.topic import TopicHandler

class StateDouble():
    
    def __init__(self):
        self.insight = []
    
    def change_topic(self, origin, channel, topic, topic_ts, channel_ts):
        self.insight.append((channel, topic, topic_ts, channel_ts))


class TopicTest(unittest.TestCase):
    
    def test_simple_change(self):
        s = StateDouble()
        c = TopicHandler(s)
        c.handle((1,1), ["#test", "8", "10", "New topic"])
        self.assertEquals([("#test", "New topic", 10, 8)], s.insight)
    
    def test_no_ts_change(self):
        s = StateDouble()
        c = TopicHandler(s)
        c.handle((1,1), ["#test", "New topic"])
        self.assertEquals([("#test", "New topic", 0, 0)], s.insight)
