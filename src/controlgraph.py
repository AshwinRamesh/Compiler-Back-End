import instruction

class Node:

    def __init__(self, block_id, instructions):
        self.node_id = block_id
        #instructions is a list of instruction objects, which we construct here.
        self.instructions = [instruction.Instruction(instr[0], instr[1:]) for instr in instructions]
        self.in_nodes = []
        self.out_nodes = []

    def add_instruction(self, instruction):
        self.instructions.append(instruction)
    
    def remove_instruction(self, instruction):
        self.instructions.remove(instruction)

    def get_registers(self):
        registers = []
        for instruction in self.instructions:
            registers += instruction.get_registers()
        #time to be a hack and remove duplicates
        registers = list(set(registers))
        return registers

    def set_id(self, block_id):
        self.node_id = block_id

    def get_id(self):
        return self.node_id

    def __iter__(self):
        return self.instructions.__iter__()

    #adds an out edge to this node and keeps track of that edge in the node we're connecting to.
    def add_out_node(self, node):
        self.out_nodes.append(node)
        node.in_nodes.append(self)

    def get_instructions(self):
        return self.instructions

    def get_in_nodes(self):
        return self.in_nodes

    def get_out_nodes(self):
        return self.out_nodes

    def __str__(self):
        return "Node ID: %s \n Instructions: %s \n Predecessors: %s \n Successors: %s \n" % \
        (self.node_id, self.instructions, [node.get_id() for node in self.in_nodes], [node.get_id() for node in self.out_nodes])

    def __repr__(self):
        return str(self)

class CFG:

    def __init__(self, name, blocks):

        self.name = name
        self.start = Node("START", [])
        self.end = Node("END", [])
        self.nodes = [self.start, self.end]
        self.current_block_number = 0

        current_instructions = []
        block_entry_nodes = {} # block id -> entry node
        #for every instruction in the block
        #if we hit a br or ret
        #then the code above this (but before any other br or rets) is a new node
        for block_id, instructions in blocks.iteritems():
            for instruction in instructions:
                current_instructions.append(instruction)
                opcode = instruction[0]
                if opcode == "ret":
                    #make a node with the current instructions, and clear the list for any later nodes
                    node = self.add_new_node(current_instructions)
                    current_instructions = []
                    node.add_out_node(self.end)
                    if block_id not in block_entry_nodes:
                        block_entry_nodes[block_id] = node
            #make a node at the end of the instructions
            if current_instructions:
                node = self.add_new_node(current_instructions)
                current_instructions = []
                if block_id not in block_entry_nodes:
                    block_entry_nodes[block_id] = node


        for node in self.get_nodes():
            for instruction in node.get_instructions():
                if instruction.get_op() == "br":
                    br_block_1, br_block_2 = instruction.get_arg(1), instruction.get_arg(2)
                    node.add_out_node(block_entry_nodes[br_block_1])
                    if (br_block_1 != br_block_2):
                        node.add_out_node(block_entry_nodes[br_block_2])

        #After we've made all the nodes, the first one in the list is the one the function will start at (not including the start and end nodes
        self.start.add_out_node(self.nodes[2])


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

    def get_registers(self):
        registers = set()
        for node in self.nodes:
            for register in node.get_registers():
                registers.add(register)
        return registers

    def get_nodes(self):
        return self.nodes
    def set_nodes(self, new_nodes):
        self.nodes = new_nodes
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

    def print_nodes(self):
        return [node.get_id() for node in self.nodes]

