from unittest import TestCase
from model import Request, Infocenter, Node
from statistic import Statistic, State, STAT_STRING

__author__ = 'akril'

class TestStatistic(TestCase):
    def test_add_req(self):
        #given
        dest = Infocenter(10, 3)
        self.statistic = Statistic([(Node()), dest])

        request = Request(0, 1, 1)

        #when
        self.statistic.add_req(request)

        #then
        self.assertIsNone(self.statistic.timeline.state_for(dest, 0))

        state = self.statistic.timeline.state_for(1, 1)
        self.assertEqual(state.start, 1)
        self.assertTrue(8 <= state.end <= 14)
        self.assertEqual(state.node, 1)


    def test_add_req_with_intersection(self):
        # given
        dest = Infocenter(10, 3)
        self.statistic = Statistic([Node(), Node(), dest])

        first = Request(0, 2, 1)
        second = Request(1, 2, 2)

        # when
        self.statistic.add_req(first)
        self.statistic.add_req(second)

        # then
        first_state = self.statistic.timeline.state_for(2, 1)
        second_state = self.statistic.timeline.state_for(2, first_state.end + 1)

        self.assertIsNotNone(second_state)
        self.assertEquals(first_state.end + 1, second_state.start)


    def test_fill_stat_string(self):
        #given
        self.statistic = Statistic([Node(), Infocenter(2, 1)])

        node_id = 1
        states = [State(node_id, 3, 8), State(node_id, 9, 15)]

        #when
        actual = self.statistic.fill_stat_string(node_id, states)

        #then
        util = ((8 - 3) + (15 - 9)) / float(100)
        expected = STAT_STRING.format(node_id=node_id, type="Infocenter", request_number=2, util=util)
        self.assertEquals(actual, expected)

