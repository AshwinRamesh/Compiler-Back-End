## Interpretter Implentation ##
## @author Ashwin Ramesh


## Imports ##
from string import whitespace


## This function will parse a lisp set exp into a more readable format in python.
# @author Paul Bonser - https://github.com/pib
def parse(sexp):
    atom_end = set('()"\'') | set(whitespace)
    stack, i, length = [[]], 0, len(sexp)
    while i < length:
        c = sexp[i]
        reading = type(stack[-1])
        if reading == list:
            if   c == '(': stack.append([])
            elif c == ')':
                stack[-2].append(stack.pop())
                if stack[-1][0] == ('quote',): stack[-2].append(stack.pop())
            elif c == '"': stack.append('')
            elif c == "'": stack.append([('quote',)])
            elif c in whitespace: pass
            else: stack.append((c,))
        elif reading == str:
            if   c == '"':
                stack[-2].append(stack.pop())
                if stack[-1][0] == ('quote',): stack[-2].append(stack.pop())
            elif c == '\\':
                i += 1
                stack[-1] += sexp[i]
            else: stack[-1] += c
        elif reading == tuple:
            if c in atom_end:
                atom = stack.pop()
                if atom[0][0].isdigit(): stack[-1].append(eval(atom[0]))
                else: stack[-1].append(atom)
                if stack[-1][0] == ('quote',): stack[-2].append(stack.pop())
                continue
            else: stack[-1] = ((stack[-1][0] + c),)
        i += 1
    return format(stack.pop()[0])


# Convert an instruction in this format: [('id',), ('bd',), ('cd',)] => ["id", "bd", "cd"]
# @author Ashwin Ramesh
def format_instruction(instructions):
    new_instuctions = []
    for instruction in instructions:
        new_instuction = []
        for param in instruction:
            if type(param) == tuple:
                new_instuction.append(param[0])
            else:
                new_instuction.append(param)
        new_instuctions.append(new_instuction)
    return new_instuctions

# correctly format the parsed lisp list
# @author Ashwin Ramesh
def format(parsed_exp):
    parsed_list = {}
    for function in parsed_exp:
        args = []
        for arg in function[1]:
            args.append(arg[0])
        blocks = {}
        for block in function[2:]:
            blocks[int(block[0])] = format_instruction(block[1:])
        parsed_list[function[0][0]] = {"args": args, "blocks": blocks}
    return parsed_list


## Process file ##
## @author Ashwin Ramesh
def process_file(file_name):
    with open(file_name):
        pass
    # read file
    with open(file_name, 'rU') as content_file:
        content = content_file.read()
    return parse(content)
