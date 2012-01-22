from statistic import Statistic

class Model(object):
	
	def __init__(self, matrix, infocenters):
		self.infocenters = infocenters
		self.nodes = [Node() for row in matrix]
		for i in range(len(matrix)):
			self.nodes[i].nodes = [self.nodes[j] for j in matrix[i] if j == 1]
			self.nodes[i].infocenter = True if i in infocenters else False

	def imitate(self, data):
		# TODO implement me
		return Statistic()

class Node(object):
	
	def __init__(self):
		pass



def create_model(matrix_file, ic_file):
	matrix_data = load_data(matrix_file)
	matrix = parse_matrix(matrix_data)

	infocenters = [int(i) - 1 for i in load_data(ic_file)[0]]
	validate_infocenters(infocenters, matrix)

	return Model(matrix, infocenters) if matrix and infocenters else None

def load_data(file):
	from csv import reader
	return [row for row in reader(open(file, 'rb'))]

def parse_matrix(data):
	matrix = []
	for row in data:
		matrix_row = []
		for num in row:
			# avoid comments that starts from # 
			if num.startswith('#'): 
				break
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
	validate(max(infocenters) + 1 <= len(matrix), 
			"There are no node with the number {} in a model, it cannot be an infocenter".format(max(infocenters) + 1))
	validate(len(infocenters) < len(matrix), "Not every node can be an infocenter")


if __name__ == "__main__":
    create_model('./example/matrix.csv', './example/infocenters.csv')