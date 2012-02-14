from unittest import TestCase
from statistic import Timeline, State

__author__ = 'akril'

class TestTimeline(TestCase):
    def setUp(self):
        self.timeline = Timeline()


    def test_add_state(self):
        # given
        state = State()
        state.node = "destination_node"
        state.start = 1
        state.end = 3

        #when
        self.timeline.add_state(state)

        #then
        self.assertEquals(self.timeline.state_for("destination_node", 1), state)
        self.assertEquals(self.timeline.state_for("destination_node", 2), state)
        self.assertEquals(self.timeline.state_for("destination_node", 3), state)

        self.assertIsNone(self.timeline.state_for("destination_node", 0))
        self.assertIsNone(self.timeline.state_for("destination_node", 4))

        self.assertIsNone(self.timeline.state_for("wrong_node", 3))


