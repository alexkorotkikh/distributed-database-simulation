from unittest import TestCase
from statistic import Timeline, State

__author__ = 'akril'

class TestTimeline(TestCase):
    def setUp(self):
        self.timeline = Timeline()


    def test_add_state(self):
        # given
        state = State("destination_node", 1, 3)

        # when
        self.timeline.add_state(state)

        # then
        self.assertEquals(self.timeline.state_for("destination_node", 1), state)
        self.assertEquals(self.timeline.state_for("destination_node", 2), state)

        self.assertIsNone(self.timeline.state_for("destination_node", 0))
        self.assertIsNone(self.timeline.state_for("destination_node", 3))

        self.assertIsNone(self.timeline.state_for("wrong_node", 1))


    def test_all_states_for_node(self):
        # given
        self.timeline.add_state(State("destination_node", 1, 3))
        self.timeline.add_state(State("destination_node", 4, 6))
        self.timeline.add_state(State("another_node", 4, 6))

        # when
        states = self.timeline.all_states_for("destination_node")

        # then
        self.assertEquals(len(states), 2)
        self.assertTrue(all([s.node == "destination_node" for s in states]))


    def test_all_states_for_moment(self):
    # given
        self.timeline.add_state(State("destination_node", 1, 3))
        self.timeline.add_state(State("destination_node", 4, 6))
        self.timeline.add_state(State("another_node", 4, 6))

        # when
        states = self.timeline.all_states_for(moment=5)

        # then
        self.assertEquals(len(states), 2)
        self.assertListEqual(sorted([s.node for s in states]), ["another_node", "destination_node"])
