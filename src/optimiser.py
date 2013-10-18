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
        cfg.set_nodes(reachable_nodes)

    @classmethod
    def remove_dead_code(self, cfg):

        def transfer(node, in_set):
            out_set = {register : used for register, used in in_set.iteritems()}
            for instruction in reversed(node.get_instructions()):
                if instruction.get_op() in ["br","ret","st"] or any(register in out_set for register in instruction.get_registers()):
                    for register in instruction.get_registers():
                        out_set[register] = True
            return out_set

        nodes = self.postorder(cfg)
        # {node -> {in set}, {out set} }
        sets = {node : [{}, {}] for node in nodes }
        worklist = copy.copy(cfg.get_end().get_in_nodes())
        while worklist:
            node = worklist[0]
            sets[node][1] = transfer(node, sets[node][0])
            for predecessor in node.get_in_nodes():
                sets[predecessor][0] = sets[node][1]
                worklist.append(predecessor)
            worklist.remove(node)

        # TRANSFORM PHASE
        for node in nodes:
            registers = node.get_registers()
            out_set = sets[node][1]
            # unused register is a register that is not in the out set.
            unused_registers = filter(lambda reg : reg not in out_set, registers)
            # remove all instructions that use this register from the nodes
            node_instructions = copy.copy(node.get_instructions())
            for instruction in node_instructions:
                #if every register in the instruction is one unused in the node, then that instruction is obsolete
                if all(register in unused_registers for register in instruction.get_registers()):
                    node.remove_instruction(instruction)

    # returns True if any changes were made
    @classmethod
    def fix_redundant_loads(self, cfg):

        #define
        IN, OUT, GEN, KILL = 0, 1, 2, 3

        nodes = self.preorder(cfg)
        sets = {node : [set(),set(),set(),set()] for node in nodes}

        # make gen and kill sets for all nodes

        def make_gen_for_node(node):
            gen = set()
            for instr in node:
                op = instr.get_op()
                # if the instruction is an operation that overwrites a register...
                if op not in ("st", "br", "ret"):
                    # remove any previous instrs in gen that use the register in this instruction
                    # gen always contains either LD or ST instructions, which contain exactly one register,
                    # hence why we use get_registers().pop() here.
                    gen = set(i for i in gen if i.get_registers().pop() != instr.get_registers().pop())

                    # if it's an ld then it should be in the gen set
                    if op == "ld":
                        gen.add(instr)

                if op == "st":
                    # remove any previous instrs that use the variable in this instruction
                    # gen always contains either LD or ST instructions, which contain exactly one variable,
                    # hence why we use get_variables().pop() here.
                    gen = set(i for i in gen if i.get_variables().pop() != instr.get_variables().pop())
                    gen.add(instr)

            return gen

        def make_kill_for_node(node):
            # the kill set contains all the instructions in the program that are "killed" by this node
            # that is, we look through every LD in the program, and see if its register is overwritten by this node.
            kill = set() 
            for instr in node:
                op = instr.get_op()
                # we don't look at instructions who don't affect a variable or register.
                if op in ("br", "ret"):
                    continue

                # getting here means instr is an instruction that may kill other instructions.
                # then go through every LD in the program, ignoring this node 
                for node2 in [n for n in cfg.get_nodes() if n != node]:
                    for instr2 in [i for i in node2 if i.get_op() == "ld"]:
                        # if the instruction is an operation that writes to a register...
                        if op not in ("st", "br", "ret"):
                            # and it writes to the same register as our killer instruction...
                            if instr2.get_registers().pop() == instr.get_registers().pop():
                                kill.add(instr2)

                        # if the instruction writes to a variable...
                        if op == "st":
                            # and it writes to the same variable as our killer instruction...
                            if instr2.get_variables().pop() == instr.get_variables().pop():
                                kill.add(instr2)
            return kill

        for node in nodes:
            sets[node][GEN] = make_gen_for_node(node)
            sets[node][KILL] = make_kill_for_node(node)

        def transfer(node, node_sets):
            return node_sets[GEN] | (node_sets[IN] - node_sets[KILL])

        worklist = copy.copy(cfg.get_start().get_out_nodes())
        while worklist:
            node = worklist[0]
            sets[node][OUT] = transfer(node, sets[node])
            for successor in node.get_out_nodes():
                sets[successor][IN] = sets[node][OUT]
                worklist.append(successor)
            worklist.remove(node)

        # TRANSFORM PHASE

        # replaces all the registers used in instructions in node that are old_reg with new_reg
        # except if the instruction is ignored_instruction. this is always a ld instruction.
        # we need to ignore it because it needs to become dead code - if we change it, optimiser
        # will think the instruction is actually needed.
        def replace_register(node, old_reg, new_reg, ignored_instruction):
            for instruction in node:
                if instruction == ignored_instruction:
                    continue
                for i in xrange(instruction.get_num_args()):
                    if instruction.get_arg(i) == old_reg:
                        instruction.set_arg(i, new_reg)

        # go through all the nodes, and find instances where
        # the in set and out set have an instruction with the same variable but different registers.
        # (i've put this in a function to make it so we can break out of that super nested for-loop below easily)
        # (it also returns True if a change was made)
        def transform():
            for node in nodes:
                for instr in sets[node][IN]:
                    for instr2 in sets[node][OUT]:
                        reg1, reg2, var1, var2 = instr.get_registers().pop(), instr2.get_registers().pop(), instr.get_variables().pop(), \
                                instr2.get_variables().pop()
                        if var1 == var2 and reg1 != reg2:
                            # so the variable is stored in both reg1 and reg2. we replace the out set register (reg2)
                            # with the in set register (reg1)
                            replace_register(node, reg2, reg1, instr2)
                            # once we've done that, we can't continue - we need to re-do this analysis. so return here.
                            return True
            return False
        return transform()
