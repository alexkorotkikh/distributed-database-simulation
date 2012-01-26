from csv import reader
from statistic import Statistic

class Model(object):
	
	def __init__(self, matrix, infocenters):
		self.infocenters = [row[0] for row in infocenters]
		self.nodes = [Node() for row in matrix]
		for i in range(len(matrix)):
			self.nodes[i].nodes = [self.nodes[j] for j in matrix[i] if j == 1]
			if i in self.infocenters:
				row = infocenters[self.infocenters.index(i)]
				self.nodes[i].infocenter = (row[1], row[2])

	def imitate(self, data):
		loaded = load_data(data)
		validate_requests(loaded)
		return Statistic()

	def validate_requests(self, requests):
		nodes = [row[0] for row in requests]
		ics = [row[1] for row in requests]
		times = [row[2] for row in requests]

		validate(max(nodes) < len(self.nodes), "Node number {} is not presented in model".format(max(nodes)))
		validate(not any([node in self.infocenters for node in nodes]), "There should be no calls from one infocenter to another")

		validate(all([ic in self.infocenters for ic in ics]), "Not all nodes in a second column is an infocenter")


class Node(object):
	
	def __init__(self):
		pass



def create_model(matrix_file, ic_file):
	matrix_data = load_matrix_data(matrix_file)
	matrix = parse_matrix(matrix_data)

	infocenters = load_data(ic_file)
	validate_infocenters(infocenters, matrix)

	return Model(matrix, infocenters) if matrix and infocenters else None

def load_matrix_data(file):
	return [row for row in reader(open(file, 'rb')) if not row[0].startswith("#")]

def load_data(file):
	return [[int(num) for num in row] for row in load_matrix_data(file)]

def parse_matrix(data):
	matrix = []
	for row in data:
		matrix_row = []
		for num in row:
			matrix_row.append(int(num))
		if matrix_row: 
			matrix.append(matrix_row)

	try:
		validate_matrix(matrix)
	except ValueError as err:
		print err
		return None
	return matrix

def validate(exp, msg):
	if not exp:
		raise ValueError(msg)

def validate_matrix(matrix):
	# validate is square
	for row in matrix:
		validate(len(row) == len(matrix), "Matrix is not square")

	# validate is symmetric
	side = range(len(matrix))
	for x in side:
		for y in side:
			validate(matrix[x][y] == matrix[y][x], 
					 "Matrix is not symmetric, check coordinates [{}, {}]".format(x, y))

def validate_infocenters(infocenters, matrix):	
	ic_nums = [row[0] for row in infocenters]
	validate(max(ic_nums) + 1 <= len(matrix), 
			"There are no node with the number {} in a model, it cannot be an infocenter".format(max(ic_nums) + 1))
	validate(len(infocenters) < len(matrix), "Not every node can be an infocenter")



if __name__ == "__main__":
    create_model('./example/matrix.csv', './example/infocenters.csv')