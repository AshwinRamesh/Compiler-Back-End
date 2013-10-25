class Instruction():
    #maps each instruction to the kind of thing it can store as arguments
    OPCODE_INFO = {
        "lc": ["REG", "NUM"],
        "ld": ["REG", "ID"],
        "st": ["ID", "REG"],
        "add": ["REG", "REG", "REG"],
        "sub": ["REG", "REG", "REG"],
        "mul": ["REG", "REG", "REG"],
        "div": ["REG", "REG", "REG"],
        "lt": ["REG", "REG", "REG"],
        "gt": ["REG", "REG", "REG"],
        "eq": ["REG", "REG", "REG"],
        "br": ["REG", "NUM", "NUM"],
        "ret": ["REG"],
        "call": ["REG", "ID", "REG_LIST"]
    }

    def __init__(self, op, args):
        self.args = args #args is a list of registers/constants/identifiers
        self.op = op

    def get_op(self):
        return self.op

    def get_registers(self):
        #a list we make sure is unique (but ordered, so we can't use a set)
        registers = []
        arg_info = self.OPCODE_INFO[self.op]
        for i in xrange(len(arg_info)):
            arg = self.args[i]
            if arg_info[i] == "REG":
                if arg not in registers:
                    registers.append(arg)
            elif arg_info[i] == "REG_LIST":
                for j in xrange(i,len(self.args)):
                    if arg not in registers:
                        registers.append(arg)
        return registers

    def _get_args_with_type(self, type_):
        ret = []
        arg_info = self.OPCODE_INFO[self.op]
        for i in xrange(len(arg_info)):
            if arg_info[i] == type_:
                if self.args[i] not in ret:
                    ret.append(self.args[i])
        return ret

    def get_variables(self):
        return self._get_args_with_type("ID")

    def get_constants(self):
        return self._get_args_with_type("NUM")

    def get_arg(self, index):
        return self.args[index]

    def get_num_args(self):
        return len(self.args)

    def set_arg(self, index, value):
        self.args[index] = value

    def __str__(self):
        return "(" + self.op + " " + " ".join(map(str, self.args)) + ")"

    def __repr__(self):
        return str(self)
