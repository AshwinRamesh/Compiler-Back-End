import parser
from controlgraph import CFG 
import sys
import optimiser

def main():
    program = parser.process_file(sys.argv[1])
    graphs = [] #dealwithit
    #for key, function in functions.items():
    #    graphs[key] = ControlGraph.create_cfg(key, function)

    for name, function in program.iteritems():
        graphs.append(CFG(name, function['blocks']))

    for graph in graphs:
        print graph
        print "Optimising...."
        optimiser.Optimiser.remove_unreachable_nodes(graph)


if __name__ == "__main__":
    main()
