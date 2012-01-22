from statistic import Statistic

class Model(object):
	
	def __init__(self, matrix):
		self.nodes = [Node() for row in matrix]
		for i in range(len(matrix)):
			self.nodes[i].nodes = [self.nodes[j] for j in matrix[i] if j == 1]

	def imitate(self, data):
		# TODO implement me
		return Statistic()

class Node(object):
	
	def __init__(self):
		pass


def create_model(file):
	data = load_data(file)
	matrix = parse_matrix(data)
	# print matrix
	return Model(matrix) if matrix else None

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


def validate_matrix(matrix):
	def validate(exp, msg):
		if not exp:
			raise ValueError(msg)

	# validate is square
	for row in matrix:
		validate(len(row) == len(matrix), "Matrix is not square")

	# validate is symmetric
	side = range(len(matrix))
	for x in side:
		for y in side:
			validate(matrix[x][y] == matrix[y][x], 
					 "Matrix is not symmetric, check coordinates [{}, {}]".format(x, y))




if __name__ == "__main__":
    create_model('./matrix.csv')