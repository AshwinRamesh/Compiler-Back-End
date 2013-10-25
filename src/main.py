import parser
from controlgraph import CFG 
import sys
import optimiser

def graphs_to_code(graphs):
    ret = "("
    for graph in graphs:
        ret += graph.create_intermediate_code()
    ret += "\n)\n"
    return ret

def main():
    program = parser.process_file(sys.argv[1])
    graphs = []

    for name, function in program.iteritems():
        graphs.append(CFG(name, function['blocks'], function['args']))

    for graph in graphs:
        #print graph
        #print "Optimising...."
        optimiser.Optimiser.remove_unreachable_nodes(graph)
        while True:
            optimiser.Optimiser.remove_dead_code(graph)
            # this returns False if no changes were made
            if optimiser.Optimiser.fix_redundant_loads(graph) == False:
                break
            print graph

    print graphs_to_code(graphs)

if __name__ == "__main__":
    main()
