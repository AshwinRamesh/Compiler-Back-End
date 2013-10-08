import parser
from controlgraph import CFG 
import sys


def main():
    program = parser.process_file(sys.argv[1])
    graphs = [] #dealwithit
    #for key, function in functions.items():
    #    graphs[key] = ControlGraph.create_cfg(key, function)

    for name, function in program.iteritems():
        graphs.append(CFG(name, function['blocks']))

    for graph in graphs:
        print graph

if __name__ == "__main__":
    main()
