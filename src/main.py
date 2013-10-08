import parser
from controlgraph import CFG 
import sys


def main():
    program = parser.process_file(sys.argv[1])
    print program
    #for key, function in functions.items():
    #    graphs[key] = ControlGraph.create_cfg(key, function)

    cfg = CFG(program)

if __name__ == "__main__":
    main()
