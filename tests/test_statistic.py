from unittest import TestCase
from model import Request, Infocenter, Node
from statistic import Statistic

__author__ = 'akril'

class TestStatistic(TestCase):
    def setUp(self):
        self.statistic = Statistic(None)


    def test_add_req(self):
        #given
        dest = Infocenter(10, 3)
        request = Request(Node(), dest, 1)

        #when
        self.statistic.add_req(request)

        #then
        self.assertEqual(self.statistic.timeline.state_for(dest, 0), None)

        state = self.statistic.timeline.state_for(dest, 1)
        self.assertEqual(state.start, 1)
        self.assertTrue(7 <= state.end <= 13)
        self.assertEqual(state.node, dest)


    def test_add_req_with_intersection(self):
        #given
        dest = Infocenter(10, 3)
        first = Request(Node(), dest, 1)
        second = Request(Node(), dest, 2)

        #when
        self.statistic.add_req(first)
        self.statistic.add_req(second)

        #then
        first_state = self.statistic.timeline.state_for(dest, 1)
        second_state = self.statistic.timeline.state_for(dest, first_state.end + 1)

        self.assertIsNotNone(second_state)
        self.assertEquals(first_state.end + 1, second_state.start)


