
## Node - represents a block of code. Will be linked together to form a Control Flow Graph (CFG)
## Attributes:
#### node_id <-- represents the block id
#### instructions <-- represents an array of instructions in the block
#### in_nodes <-- array of nodes that point to self (predessor nodes)
#### out_nodes <-- array of nodes that represents nodes pointed to by self (successor nodes)
class Node:

    def __init__(self, block_id, instructions):
        self.node_id = block_id
        self.instructions = instructions
        self.in_nodes = []
        self.out_nodes = []

    def add_instruction(self, instruction):
        self.instructions.append(instruction)

    def get_instructions(self):
        return self.instructions

    def set_id(self, block_id):
        self.node_id = block_id

    def get_id(self):
        return self.node_id

    def add_out_node(self, node):
        self.out_nodes.append(node)
        node.in_nodes.append(self)

    def get_in_nodes(self):
        return self.in_nodes

    def get_out_nodes(self):
        return self.out_nodes

    def __str__(self):
        return "Node ID: %s \n Instructions: %s \n Predecessors: %s \n Successors: %s \n" % \
    (self.node_id, self.instructions, [node.get_id() for node in self.in_nodes], [node.get_id() for node in self.out_nodes])

    def __repr__(self):
        return str(self)


## Instruction - represents a single instruction
class Instruction:

    def __init__(self,instruction):
        self.type = instruction[0]
        self.args = instruction[1:]

    def get_type(self):
        return self.type

    def get_args(self):
        return self.args


## Block - represents a singble block --> contains many nodes
class Block:

    def __init__(self, block):
        pass


## CFG -- represents a Control Flow Graph. This holds auxillary information about nodes and performs
##        important functions such as creating the graph and creating code from nodes
## Attributes:
#### name
#### head --> start of the function. first block (0)
#### end
#### nodes
####
class CFG:

    def __init__(self, name, blocks):
        self.name = name
        self.start = Node("START", [])
        self.end = Node("END", [])
        self.nodes = [self.start, self.end]
        self.current_block_number = 0

        current_instructions = []
        #for every instruction in the block
        #if we hit a br or ret
        #then the code above this (but before any other br or rets) is a new node
        #keep going
        for block_id, instructions in blocks.iteritems():

            for instruction in instructions:
                current_instructions.append(instruction)
                operator = instruction[0]
                if operator in ("br", "ret"):
                    #make a node with the current instructions, and clear the list for any later nodes
                    node = self.add_new_node(current_instructions)
                    current_instructions = []
                    if operator == "ret":
                        node.add_out_node(self.end)

            #make a node at the end of the instructions
            if current_instructions:
                self.add_new_node(current_instructions)
                current_instructions = []

        #After we've made all the nodes, the first one in the list is the one the function will start at
        self.start.add_out_node(self.nodes[0])


    def add_new_node(self, current_instructions):
        node = Node(self.current_block_number, current_instructions)
        self.add_node(node)
        self.current_block_number += 1
        return node

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end

    def add_node(self, node):
        self.nodes.append(node)

    def get_nodes(self):
        return self.nodes

    def get_node(self, node_id):
        #TODO: map id -> node if we do this a lot
        #linearsearch
        for node in self.nodes:
            if node.get_id() == node_id:
                return node

    def create_intermediate_code(self): # TODO
        pass

    def __repr__(self):
        return self.name + ':\n' + repr(self.nodes)

