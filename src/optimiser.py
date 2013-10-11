import copy
class Optimiser():

    @staticmethod
    def dfs(cfg):
        #TODO: Is our graph ever going to be cyclic? If it is dfs will go forever, and we need to mark nodes as visited etc.
        reachable_nodes = []
        nodes = [cfg.get_start()]
        while nodes:
            for node in nodes:
                nodes.remove(node)
                nodes += node.get_out_nodes()
                reachable_nodes.append(node)
        return reachable_nodes

    @classmethod
    def remove_unreachable_nodes(self, cfg):
        reachable_nodes = self.dfs(cfg)
        #filter out and nodes that aren't reachable, and set the cfg's nodes to the new filtered list
        cfg.set_nodes(filter(lambda node : node in reachable_nodes, cfg.get_nodes()))


    @classmethod
    def remove_dead_code(self, cfg):

        def transfer(node, in_set):
            out_set = {}
            for instruction in node.get_instructions():
                if instruction.get_op() in ["br","ret","st"]:
                    for register in instruction.get_registers():
                        out_set[register] = True
                    
                else:
                    for register in instruction.get_registers():
                        if out_set.get(register,None) != True:
                            out_set[register] = False
                            
            return out_set

        nodes = self.dfs(cfg)
        # {node -> {in set}, {out set} }
        sets = {node : ({register : None for register in node.get_registers()}, {register : None for register in node.get_registers()}) for node in nodes }
        worklist = cfg.get_start().get_out_nodes()
        while worklist:
            for node in worklist:
                sets[node][1] = transfer(node, sets[node][0])
                for successor in node.get_out_nodes():
                    #sets[successor][0] = sets[node][1]
                    worklist.append(successor)
                worklist.remove(node)

        for node in nodes:
            registers = node.get_registers()
            out_set = sets[node][1]
            unused_registers = filter( lambda reg : out_set[reg] != True, registers)
            print [node.get_id(), registers, unused_registers]
            #remove all instructions that use this register from the nodes
            node_instructions = copy.copy(node.get_instructions())
            for instruction in node_instructions:
                if all(register in unused_registers for register in instruction.get_registers()):
                    node.remove_instruction(instruction)



