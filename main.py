__author__ = 'alexander.korotkikh'

import sys
from optparse import OptionParser
from model import create_model

def create_parser():
    parser = OptionParser()
    parser.add_option("-m", "--matrix", dest="matrix", 
                        help="file with model description", default="./example/matrix.csv")
    parser.add_option("-i", "--infocenters", dest="infocenters",
                        help="file with numbers of infocenters", default="./example/infocenters.csv")
    parser.add_option("-r", "--requests", dest="requests", 
                        help="file with data about requests", default="./example/requests.csv")
    return parser


def start(args):
    print "### Imitation started ###"

    parser = create_parser()
    (options, args) = parser.parse_args(args)
    model = create_model(options.matrix, options.infocenters)

    if not model:
        print "### Imitation finished unsuccessfully because of error ###"
        return;

    statistic = model.imitate(options.requests)
    print statistic.to_report()

    print "### Imitation finished successfully ###"

if __name__ == "__main__":
    start(sys.argv)