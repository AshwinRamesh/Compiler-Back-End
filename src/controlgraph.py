
## Node - represents a block of code. Will be linked together to form a Control Flow Graph (CFG)
## Attributes:
#### node_id <-- represents the block id
#### instructions <-- represents an array of instructions in the block
#### in_nodes <-- array of nodes that point to self (predessor nodes)
#### out_nodes <-- array of nodes that represents nodes pointed to by self (successor nodes)
class Node:

    def __init__(self, block_id, node_id, instructions = []):
        self.block_id = block_id
        self.node_id = node_id
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

    def get_block_id(self):
        return self.block_id

    def add_out_node(self, node):
        self.out_nodes.append(node)
        node.in_nodes.append(self)
       #print self.out_nodes
       #print "----"

    def get_in_nodes(self):
        return self.in_nodes

    def get_out_nodes(self):
        return self.out_nodes

    def get_final_instruction(self):
        return self.instructions[-1]

    def __str__(self):
        return "Block ID: %s \n Node ID: %s \n Instructions: \n%s \n Predecessors: %s \n Successors: %s \n" % \
    (self.block_id, self.node_id, self.instructions, [node.simple_str() for node in self.in_nodes], [node.simple_str() for node in self.out_nodes])

    def __repr__(self):
        return str(self)

    def simple_str(self):
        return "Block: %s Node: %s" %(self.block_id, self.node_id)


## Instruction - represents a single instruction
class Instruction:

    def __init__(self,instruction):
        self.type = instruction[0]
        self.args = instruction[1:]

    def get_type(self):
        return self.type

    def get_args(self):
        return self.args

    def __str__(self):
        return "%s\n" %(str([self.type] + self.args))

    def __repr__(self):
        return str(self)

## Block - represents a singble block --> contains many nodes
class Block:

    def __init__(self, block_id, instructions):
        self.id = block_id
        self.nodes = []
        current_instructions = [] # current sequence of instructions
        i = 0 # block node counter

        # Process all instructions and create nodes
        for instruction in instructions:
            inst = Instruction(instruction)
            current_instructions.append(inst)
            if inst.get_type() in ("br", "ret"):
                self.nodes.append(Node(block_id, i, current_instructions))
                i += 1
                current_instructions = []

        # Create another node if instructions still unprocessed
        if len(current_instructions) > 0:
            self.nodes.append(Node(block_id, i, current_instructions))

    def get_nodes(self):
        return self.nodes

    def get_id(self):
        return self.id

    def get_head(self): # return the starting node for the block
        return self.nodes[0]

    def __str__(self):
        return "%s \n-----------------\n" %(str(self.nodes))

    def __repr__(self):
        return str(self)

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
        self.end = Node(-1, 0)
        self.start = Node("START", [])
        self.blocks = []
        self.nodes = [self.end]
        self.current_block_number = 0

        # Create all nodes by creating blocks
        for block_id, instructions in blocks.items():
            self.blocks.append(Block(block_id, instructions))

        # Create all connections between nodes
        for block in self.blocks:
            for node in block.get_nodes():
                self.add_node(node)
                instruction = node.get_final_instruction()
                if (instruction.get_type() == "br"):
                    node.add_out_node(self.blocks[int(instruction.get_args()[1])].get_head())
                    node.add_out_node(self.blocks[int(instruction.get_args()[2])].get_head())
                elif (instruction.get_type() == "ret"):
                    node.add_out_node(self.end)
                else: # do i need to consider call etc? ???? TODO
                    pass

        # Set the start/head node
        self.start = self.blocks[0].get_head()


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
        return self.name + ':\n' + repr(self.blocks)

