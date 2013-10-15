import copy
class Optimiser():

    @staticmethod
    def _order(cfg, post):
        reachable_nodes = []
        nodes = [cfg.get_start()]
        prevNode = None
        while nodes:
            if post:
                node = nodes[-1]
            else:
                node = nodes[0]
            if prevNode == None or node in prevNode.get_out_nodes():
                nodes += node.get_out_nodes() 
            else:
                reachable_nodes.append(node)
                if post:
                    nodes.pop()
                else:
                    nodes.pop(0)
            prevNode = node
        return reachable_nodes

    @classmethod
    def postorder(self, cfg):
        return self._order(cfg, post=True)

    @classmethod
    def preorder(self, cfg):
        return self._order(cfg, post=False)

    @classmethod
    def remove_unreachable_nodes(self, cfg):
        reachable_nodes = self.postorder(cfg)
        #filter out and nodes that aren't reachable, and set the cfg's nodes to the new filtered list
        cfg.set_nodes(filter(lambda node : node in reachable_nodes, cfg.get_nodes()))



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

        @classmethod
        def remove_redundant_loads(self, cfg):

            #define
            IN, OUT, GEN, KILL = 0, 1, 2, 3



            def transfer(node_sets):
                #basedguido
                return node_sets[GEN] | (node_sets[IN] - node_sets[KILL])

            nodes = self.preorder(cfg)
            # {node -> {in set}, {out set} }
            sets = {node : [set(node.get_in_nodes()), set(), set(), set()] for node in nodes }
            worklist = cfg.get_start().get_out_nodes()

            while nodes:
                node = worklist[0]

                sets[node][1] = transfer(node, sets[node])
                for predecessor in node.get_in_nodes():
                    sets[predecessor][0] = sets[node][1]
                    worklist.append(predecessor)
                worklist.remove(node)



