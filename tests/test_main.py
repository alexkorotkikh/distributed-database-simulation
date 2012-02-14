from unittest import TestCase
from main import Application

__author__ = 'akril'

class TestLoadData(TestCase):
    def setUp(self):
        self.app = Application()

    def test_create_parser(self):
        options = self.app.get_options(None)
        self.assertEquals("./example/nodes.csv", options.nodes)
        self.assertEquals("./example/infocenters.csv", options.infocenters)
        self.assertEquals("./example/requests.csv", options.requests)


    def test_load_matrix_data(self):
        file_name = "../example/nodes.csv"
        matrix = self.app.load_matrix_data(file_name)

        self.assertEqual(len(matrix), 7)

    def test_validate_nodes_matrix_invalid(self):
        self.assertRaises(ValueError, self.app.validate_nodes_matrix, [[0, 0], [0]])
        self.assertRaises(ValueError, self.app.validate_nodes_matrix, [[0, 0], [1, 0]])

    def test_validate_nodes_matrix_valid(self):
        try:
            matrix = [
                [0, 1, 0],
                [1, 1, 0],
                [0, 0, 0]
            ]
            self.app.validate_nodes_matrix(matrix)
        except Exception:
            self.fail("Shouldn't raise exception on valid matrix")

    def test_validate_infocenters_invalid(self):
        self.app.nodes = [[0, 1], [1, 0]]
        self.assertRaises(ValueError, self.app.validate_infocenters_matrix, [[3, 0, 0]])
        self.assertRaises(ValueError, self.app.validate_infocenters_matrix, [[1, 2, 1], [2, 4, 2]])

    def test_validate_infocenters_matrix_valid(self):
        try:
            self.app.nodes = [
                [0, 1, 0],
                [1, 1, 0],
                [0, 0, 0]
            ]
            self.app.validate_infocenters_matrix([[1, 5, 2]])
            self.app.validate_infocenters_matrix([[1, 2, 1], [2, 4, 2]])
        except Exception:
            self.fail("Shouldn't raise exception on valid data")

    def test_validate_request_matrix_valid(self):
        try:
            self.app.nodes = [
                [0, 1, 0],
                [1, 1, 0],
                [0, 0, 0]
            ]
            self.app.infocenters = [[2, 5, 2]]
            self.app.validate_request_matrix([[1, 2, 1]])
        except Exception:
            self.fail("Shouldn't raise exception on valid data")

    def test_validate_request_matrix_invalid(self):
        self.app.nodes = [
            [0, 1, 0],
            [1, 1, 0],
            [0, 0, 0]
        ]
        self.app.infocenters = [[2, 5, 2]]

        self.assertRaises(ValueError, self.app.validate_request_matrix, [[4, 1, 1]])
        self.assertRaises(ValueError, self.app.validate_request_matrix, [[1, 3, 1]])
