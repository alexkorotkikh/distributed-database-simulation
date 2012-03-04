from statistic import Statistic

class Model(object):
    def __init__(self, nodes, infocenters):
        self.nodes = [Node() for row in nodes]
        for row in infocenters:
            self.nodes[row[0]] = Infocenter(row[1], row[2])

        for i in range(len(nodes)):
            self.nodes[i].nodes = [self.nodes[j] for j in nodes[i] if j == 1]


    def imitate(self, req_matrix):
        requests = self.create_request_list(req_matrix)

        requests.sort(lambda x, y: x.start - y.start)

        # start immitating
        stat = Statistic(self.nodes)

        for request in requests:
            stat.add_req(request)

        return stat


    def create_request_list(self, req_matrix):
        def list_portion(req_matrix):
            return [Request(row[0], row[1], row[2]) for row in req_matrix]

        requests = list_portion(req_matrix)
        while requests[-1].start < 1000:
            new_req_matrix = [[row[0], row[1], row[2] + row[3], row[3]] for row in req_matrix]
            requests.extend(list_portion(new_req_matrix))
            req_matrix = new_req_matrix

        return requests


class Node(object):
    def __init__(self):
        pass


class Infocenter(Node):
    def __init__(self, average, deviation):
        self.average = average
        self.deviation = deviation


class Request:
    def __init__(self, src, dest, start):
        self.src = src
        self.dest = dest
        self.start = start
