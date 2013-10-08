class Node:

    def __init__(self, block_id, instructions):
        self.node_id = block_id
        self.instructions = instructions
        self.in_nodes = []
        self.out_nodes = []

    def add_instruction(self, instruction):
        self.instructions.append(instruction)

    def set_id(self, block_id):
        self.node_id = block_id

    def get_id(self):
        return self.node_id

    def add_in_node(self, node):
        self.in_nodes.append(node)

    def add_out_node(self, node):
        self.out_nodes.append(node)

    def get_instructions(self):
        return self.instructions

    def get_in_nodes(self):
        return self.in_nodes

    def get_out_nodes(self):
        return self.out_nodes

    def __str__(self):
        return "Node ID: %s \n Instructions: %s \n Predecessors: %s \n Successors: %s \n" % (self.node_id, self.instructions, self.in_nodes, self.out_nodes)
    def __repr__(self):
        return str(self)

class CFG:

    def __init__(self, blocks):
        #TODO: Are we the worst?
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

                if instruction[0] in ("br", "ret"):
                    #make a node with the current instructions, and clear the list for any later nodes
                    self.add_new_node(current_instructions)
                    current_instructions = []
            #make a node at the end of the instructions
            if current_instructions:
                self.add_new_node(current_instructions)
                current_instructions = []



        print self.nodes


    def add_new_node(self, current_instructions):
        node = Node(self.current_block_number, current_instructions)
        self.add_node(node)
        self.current_block_number += 1

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

