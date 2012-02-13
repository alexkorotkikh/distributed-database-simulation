import unittest
from model import Model, Infocenter
from model import Node

class TestModel(unittest.TestCase):
    def test_model_constructor(self):
        matrix = [[0, 1], [1, 0]]
        infocenters = [[1, 5, 2]]
        model = Model(matrix, infocenters)

        self.assertEquals(2, len(model.nodes))
        self.assertIsInstance(model.nodes[0], Node)
        self.assertIsInstance(model.nodes[1], Infocenter)

        self.assertIs(model.nodes[0].nodes[0], model.nodes[1])
        self.assertIs(model.nodes[1].nodes[0], model.nodes[1])

        self.assertEquals((5, 2), (model.nodes[1].average, model.nodes[1].deviation))


if __name__ == '__main__':
    unittest.main()








		