import unittest
from model import validate_matrix
from model import create_model
from model import Model
from model import Node
from main import create_parser

class TestMainModule(unittest.TestCase):
    def test_create_parser(self):
        (options, args) = create_parser().parse_args()
        self.assertEquals("./example/nodes.csv", options.matrix)
        self.assertEquals("./example/infocenters.csv", options.infocenters)
        self.assertEquals("./example/requests.csv", options.requests)


class TestModel(unittest.TestCase):
    def test_create_model(self):
        model = create_model("./example/nodes.csv", "./example/infocenters.csv")
        self.assertEquals(7, len(model.nodes))

    def test_model_constructor(self):
        matrix = [[0, 1], [1, 0]]
        infocenters = [[1, 5, 2]]
        model = Model(matrix, infocenters)

        self.assertEquals(2, len(model.nodes))
        self.assertIsInstance(model.nodes[0], Node)
        self.assertIsInstance(model.nodes[1], Node)

        self.assertIs(model.nodes[0].nodes[0], model.nodes[1])
        self.assertIs(model.nodes[1].nodes[0], model.nodes[1])

        self.assertEquals((5, 2), model.nodes[1].infocenter)

    def test_model_imitate(self):
        model = create_model("./example/nodes.csv", "./example/infocenters.csv")
        model.imitate("./example/requests.csv")


if __name__ == '__main__':
    unittest.main()








		