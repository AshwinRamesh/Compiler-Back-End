class Instruction():

    def __init__(self, op, args):
        self.args = args #args is a list of registers/constants/identifiers
        self.op = op
        #filter out arguments that aren't of the form r<number>
        self.registers = filter(lambda arg : str(arg).startswith('r') and len(arg) == 2 and arg[1] in "0123456789", args)

    def get_op(self):
        return self.op

    #get the number of the register. 
    #eg 'r4' -> 4
    @staticmethod
    def get_number(register):
        return int(register[1])

    def get_registers(self):
        return self.registers

    def get_args(self):
        return self.args

    def __str__(self):
        return "( " + self.op + " " + " ".join(map(str, self.args)) + " )"

    def __repr__(self):
        return str(self)
