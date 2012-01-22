import unittest
from model import validate_matrix
from model import Model
from model import Node
from main import create_parser

class TestMainModule(unittest.TestCase):

	def test_create_parser(self):
		(options, args) = create_parser().parse_args()
		self.assertEquals("./matrix.csv", options.matrix)
		self.assertIn("./requests.csv", options.requests)



class TestModel(unittest.TestCase):

	def test_validate_matrix_invalid(self):
		self.assertRaises(ValueError, validate_matrix, [[0,0],[0]])
		self.assertRaises(ValueError, validate_matrix, [[0,0],[1,0]])

	def test_validate_matrix_valid(self):
		try:
			matrix = [
				[0, 1, 0],
				[1, 1, 0],
				[0, 0, 0]
			]
			validate_matrix(matrix)
		except Exception:
			self.fail("Shouldn't raise exception on valid matrix")
			
	def test_model_creation(self):
		matrix = [[0,1],[1,0]]
		model = Model(matrix)

		self.assertEquals(2, len(model.nodes))
		self.assertIsInstance(model.nodes[0], Node)
		self.assertIsInstance(model.nodes[1], Node)

		self.assertIs(model.nodes[0].nodes[0], model.nodes[1])
		self.assertIs(model.nodes[1].nodes[0], model.nodes[1])

				


if __name__ == '__main__':
    unittest.main()








		