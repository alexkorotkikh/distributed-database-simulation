import unittest
from model import validate_matrix
from model import validate_infocenters
from model import Model
from model import Node
from main import create_parser

class TestMainModule(unittest.TestCase):

	def test_create_parser(self):
		(options, args) = create_parser().parse_args()
		self.assertEquals("./example/matrix.csv", options.matrix)
		self.assertEquals("./example/infocenters.csv", options.infocenters)
		self.assertEquals("./example/requests.csv", options.requests)



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

	def test_validate_infocenters_invalid(self):
		self.assertRaises(ValueError, validate_infocenters, [3], [[0,1],[1,0]])
		self.assertRaises(ValueError, validate_infocenters, [1, 2], [[0,1],[1,0]])

	def test_validate_infocenters_valid(self):
		try:
			matrix = [
				[0, 1, 0],
				[1, 1, 0],
				[0, 0, 0]
			]
			validate_infocenters([1], matrix)
			validate_infocenters([1, 2], matrix)
		except Exception:
			self.fail("Shouldn't raise exception on valid matrix")
								
	def test_model_creation(self):
		matrix = [[0,1],[1,0]]
		infocenters = [1]
		model = Model(matrix, infocenters)

		self.assertEquals(2, len(model.nodes))
		self.assertIsInstance(model.nodes[0], Node)
		self.assertIsInstance(model.nodes[1], Node)

		self.assertIs(model.nodes[0].nodes[0], model.nodes[1])
		self.assertIs(model.nodes[1].nodes[0], model.nodes[1])

				


if __name__ == '__main__':
    unittest.main()








		