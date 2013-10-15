import copy
class Optimiser():

    @staticmethod
    def postorder(cfg):
        reachable_nodes = []
        nodes = [cfg.get_start()]
        prevNode = None
        while nodes:
            node = nodes[-1]
            if prevNode == None or node in prevNode.get_out_nodes():
                nodes += node.get_out_nodes() 
            else:
                reachable_nodes.append(node)
                nodes.pop()
            prevNode = node
        return reachable_nodes

    @classmethod
    def remove_unreachable_nodes(self, cfg):
        reachable_nodes = self.postorder(cfg)
        cfg.set_nodes(reachable_nodes)

    @classmethod
    def remove_dead_code(self, cfg):

        def transfer(node, in_set):
            out_set = {register : used for register, used in in_set.iteritems()}
            for instruction in reversed(node.get_instructions()):
                if instruction.get_op() in ["br","ret","st"] or any(register in out_set for register in instruction.get_registers()):
                    for register in instruction.get_registers():
                        out_set[register] = True
            print "used registers for node", node.get_id(), ":", out_set.keys()
            return out_set

        nodes = self.postorder(cfg)
        # {node -> {in set}, {out set} }
        sets = {node : [{}, {}] for node in nodes }
        worklist = cfg.get_end().get_in_nodes()
        while worklist:
            node = worklist[0]
            sets[node][1] = transfer(node, sets[node][0])
            for predecessor in node.get_in_nodes():
                sets[predecessor][0] = sets[node][1]
                worklist.append(predecessor)
            worklist.remove(node)

        # TRANSFORM PHASE
        print "[node, all registers, unused]"
        for node in nodes:
            registers = node.get_registers()
            out_set = sets[node][1]
            # unused register is a register that is not in the out set.
            unused_registers = filter(lambda reg : reg not in out_set, registers)
            print [node.get_id(), registers, unused_registers]
            # remove all instructions that use this register from the nodes
            node_instructions = copy.copy(node.get_instructions())
            for instruction in node_instructions:
                #if every register in the instruction is one unused in the node, then that instruction is obsolete
                if all(register in unused_registers for register in instruction.get_registers()):
                    node.remove_instruction(instruction)
