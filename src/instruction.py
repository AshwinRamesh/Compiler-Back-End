import re
class Instruction():

    def __init__(self, op, args):
        self.args = args #args is a list of registers/constants/identifiers
        self.op = op
        self.update_registers()

    def update_registers(self):
        #filter out arguments that aren't of the form r<number>
        self.registers = filter(lambda arg : re.match(r'^r[0-9]+$', str(arg)), self.args)

    def get_op(self):
        return self.op

    def get_registers(self):
        return self.registers

    def get_arg(self, index):
        return self.args[index]

    def get_num_args(self):
        return len(self.args)

    def set_arg(self, index, value):
        self.args[index] = value
        self.update_registers()

    def __str__(self):
        return "( " + self.op + " " + " ".join(map(str, self.args)) + " )"

    def __repr__(self):
        return str(self)
