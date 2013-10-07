import parser
from optimisation_exceptions import *
from controlgraph import ControlNode, ControlGraph
import sys

functions = {}

def main():
    global functions
    try:
        if len(sys.argv) <= 1:
            raise FileNotGivenException()
        graphs = {}
        functions = parser.process_file(sys.argv[1])
        print functions
        for key, function in functions.items():
            graphs[key] = ControlGraph.create_cfg(key, function)
    except IOError:
        print "Error: File does not exist. Cannot optimise."
        exit(1)
    except FileNotGivenException as e:
        print "Error: No input file given. Cannot optimise."
        exit(1)
    #except IndexError:
    #    print "Error: Corrupted intermediate file. Cannot optimise."
    #    exit(1)


if __name__ == "__main__":
    main()
