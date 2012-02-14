import sys
from _csv import reader
from optparse import OptionParser

__author__ = 'alexander.korotkikh'

class Application:
    def start(self, args):
        print "### Imitation started ###"

        try:
            options = self.get_options(args)

            self.nodes = self.load_nodes(options.nodes)
            self.infocenters = self.load_infocenters(options.infocenters)
            model = create_model(self.nodes, self.infocenters)

            self.requests = self.load_requests(options.requests)
            statistic = model.imitate(self.requests)
            print statistic.to_report()
        except Exception as e:
            print e.message
            print "### Imitation finished unsuccessfully because of error ###"
            return;

        print "### Imitation finished successfully ###"


    def get_options(self, args):
        parser = self.create_parser()
        (options, args) = parser.parse_args(args)
        return options


    def create_parser(self):
        parser = OptionParser()
        parser.add_option("-m", "--nodes", dest="nodes",
            help="file with model description", default="./example/nodes.csv")
        parser.add_option("-i", "--infocenters", dest="infocenters",
            help="file with numbers of infocenters", default="./example/infocenters.csv")
        parser.add_option("-r", "--requests", dest="requests",
            help="file with data about requests", default="./example/requests.csv")
        return parser


    def load_nodes(self, nodes):
        matrix = self.load_matrix_data(nodes)
        self.validate_nodes_matrix(matrix)
        return matrix


    def validate(self, exp, msg):
        if not exp:
            raise ValueError(msg)


    def validate_nodes_matrix(self, matrix):
        # validate is square
        for row in matrix:
            self.validate(len(row) == len(matrix), "Matrix is not square")

        # validate is symmetric
        side = range(len(matrix))
        for x in side:
            for y in side:
                self.validate(matrix[x][y] == matrix[y][x],
                    "Matrix is not symmetric, check coordinates [{}, {}]".format(x, y))


    def load_infocenters(self, infocenters):
        matrix = self.load_matrix_data(infocenters)
        self.validate_infocenters_matrix(matrix)
        return matrix


    def validate_infocenters_matrix(self, matrix):
        ic_nums = [row[0] for row in matrix]
        self.validate(max(ic_nums) + 1 <= len(self.nodes),
            "There are no node with the number {} in a model, it cannot be an infocenter".format(max(ic_nums) + 1))


    def load_requests(self, requests):
        matrix = self.load_matrix_data(requests)
        self.validate_request_matrix(matrix)
        return matrix


    def validate_request_matrix(self, matrix):
        sources = [row[0] for row in matrix]
        destinations = [row[1] for row in matrix]

        self.validate(max(sources) < len(self.nodes),
            "Node number {} is not presented in model".format(max(sources)))

        ic_numbers = [row[0] for row in self.infocenters]
        self.validate(all([ic in ic_numbers for ic in destinations]),
            "Not all nodes presented as infocenters actually are infocenters")


    def load_matrix_data(self, file):
        def is_comment(row):
            return row[0].startswith("#")

        return [map(int, row) for row in reader(open(file, 'rb')) if not is_comment(row)]


if __name__ == "__main__":
    Application().start(sys.argv)