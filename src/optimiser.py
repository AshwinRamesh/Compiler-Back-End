
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

        def transfer(register, instruction):
            #TODO check the register isn't used in another instruction later
            return instruction.get_op() in ["br", "ret", "st"]

        nodes = self.dfs(cfg)
        # {node -> {in set}, {out set} }
        sets = {node : ({register : None for register in node.get_registers()}, {}) for node in nodes }
        worklist = cfg.get_start().get_out_nodes()
        while worklist:
            for node in worklist:
                for instruction in node.get_instructions():
                    for register in instruction.get_registers():
                        #each register needs to know which instruction it's in.
                        #the transfer function should take an in set
                        out_set = sets[node][1]
                        #get the old value in the dictionary, or None if the dictionary is empty/ the node is not there
                        old_value = out_set.get(register, None)
                        new_value = transfer(register, instruction)
                        out_set[register] = new_value
                        if old_value != new_value:
                            for successor in node.get_out_nodes():
                                sets[successor][0][register] = new_value
                                worklist.append(successor)
                worklist.remove(node)

        for node in nodes:
            registers = node.get_registers()
            out_set = sets[node][1]
            unused_registers = filter( lambda reg : out_set[reg] != True, registers)

            #remove all instructions that use this register from the nodes
            for instruction in node.get_instructions():
                if all(register in unused_registers for register in instruction.get_registers()):
                    node.remove_instruction(instruction)



