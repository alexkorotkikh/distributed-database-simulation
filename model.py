from statistic import Statistic

class Model(object):
    def __init__(self, matrix, infocenters):
        self.infocenters = [row[0] for row in infocenters]
        self.nodes = [Node() for row in matrix]
        for i in range(len(matrix)):
            if i in self.infocenters:
                row = infocenters[self.infocenters.index(i)]
                self.nodes[i] = Infocenter(row[1], row[2])

            self.nodes[i].nodes = [self.nodes[j] for j in matrix[i] if j == 1]

    def imitate(self, data):
        requests = load_data(data)
        self.validate_requests(requests)

        requests.sort()

        # start immitating
        stat = Statistic(self.nodes, self.infocenters)

        for request in requests:
            stat.add_req(request)

        return stat


class Node(object):
    def __init__(self):
        pass


class Infocenter(Node):
    def __init__(self, average, deviation):
        self.average = average
        self.deviation = deviation


def create_model(matrix_file, ic_file):
    matrix_data = load_matrix_data(matrix_file)
    matrix = parse_matrix(matrix_data)

    infocenters = load_data(ic_file)
    validate_infocenters(infocenters, matrix)

    return Model(matrix, infocenters) if matrix and infocenters else None


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


def validate_infocenters(infocenters, matrix):
    ic_nums = [row[0] for row in infocenters]
    validate(max(ic_nums) + 1 <= len(matrix),
        "There are no node with the number {} in a model, it cannot be an infocenter".format(max(ic_nums) + 1))
    validate(len(infocenters) < len(matrix), "Not every node can be an infocenter")


if __name__ == "__main__":
    create_model('./example/nodes.csv', './example/infocenters.csv')