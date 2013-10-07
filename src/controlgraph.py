# @author Ashwin Ramesh
## This class defines both the node and the graph of the control flow graph ##

class ControlNode:

    def __init__(self, block_id, instructions):
        # TODO check if instructions is array
        self.id = int(block_id)
        self.instructions = instructions
        self.pre_nodes = {}
        self.suc_nodes = {}

    def set_instructions(self, instructions):
        # TODO check if instuctions is array
        self.instructions = instructions
        return True

    def add_instruction(self, instruction):
        self.instructions.append(instruction)

    def set_id(self, block_id):
        self.id = block_id

    def set_predecessor(self, pre_node):
        if pre_node == None:
            self.pre_nodes = None
            return True
        if pre_node.id not in self.pre_nodes:
            self.pre_nodes[pre_node.id] = pre_node
            return True
        return False

    def set_successor(self, suc_node):
        if suc_node == None:
            self.suc_nodes = None
            return True
        if suc_node.id not in self.suc_nodes:
            self.suc_nodes[suc_node.id] = suc_node
            return True
        return False

    def get_instructions(self):
        return self.instructions

    def get_instruction_by_key(self, key): # TODO
        pass

    def get_predecessors(self):
        return self.pre_nodes

    def get_successors(self):
        return self.suc_nodes

    def to_str(self):
        if type(self.pre_nodes) is dict or type(self.pre_nodes) is list:
            pre_str = str(self.pre_nodes.keys())
        else:
            pre_str = "None"
        if type(self.suc_nodes) is dict or type(self.suc_nodes) is list:
            suc_str = str(self.suc_nodes.keys())
        else:
            suc_str = "None"
        return "Node ID: %d \n Instructions: %s \n Predecessors: %s \n Successors: %s \n" %(self.id, str(self.instructions), pre_str, suc_str)

class ControlGraph:

    def __init__(self, function_name):
        self.name = function_name
        self.nodes = {}

    def set_head(self, head_node):
        self.head = head_node
        head_node.set_predecessor(None)

    def get_head(self):
        return self.head

    def add_node(self, node):
        if not self.check_node_exists(node.id):
            self.nodes[node.id] = node # place in array by block id key
            return True
        return False

    def get_nodes(self):
        return self.nodes

    def get_node(self, id):
        if self.check_node_exists(id):
            return self.nodes[id]
        return False

    def create_intermediate_code(self): # TODO
        pass

    def check_node_exists(self, id):
        if id in self.nodes:
            return True
        return False

    @staticmethod
    def create_cfg(name, function):
        blocks = function['blocks']
        if len(blocks) < 0:
            return False
        g = ControlGraph(name)
        # Add the nodes
        for block_id, block in blocks.items():
            node = ControlNode(block_id, block)
            g.add_node(node)
        # Make nodes directed and joint
        for block_id, block in blocks.items():
            node = g.nodes[block_id]
            if block_id == 0:
                g.set_head(node) # Set head node
            last_instruction = block[-1]
            if last_instruction[0] == "br": # last instruction is branching
                node_true = g.nodes[int(last_instruction[2])] # branching node for true
                node_false = g.nodes[int(last_instruction[3])] # branching node for false
                # Set pre/succ
                node.set_successor(node_true)
                node.set_successor(node_false)
                node_true.set_predecessor(node)
                node_false.set_predecessor(node)
            if last_instruction[0] == "ret": # last instruction is return
                node.set_successor(None)
        g.print_graph()
        return g

    def print_graph(self):
        print "Graph of function: %s \n" %(self.name)
        for key, node in self.nodes.items():
            print node.to_str()
