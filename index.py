DEBUG = False
exp1 = "1 + 1 *2"
exp2 = "(1+ 12 * 3) + ((4) + 6 -8)"

def eval_tokens(left, op, right):
    if left[0] != 'int' or op[0] != 'operator' or right[0] != 'int':
        return None
    match op[1]:
        case '+':
            return left[1] + right[1]
        case '-':
            return left[1] - right[1]
        case '*':
            return left[1] * right[1]
        case '/':
            return int(left[1] / right[1])
    return None

def eval_num_expression(exp: str, tab_cout = 0):
    # Clear white space
    tab = tab_cout * "\t"
    exp = exp.replace(" ", "").replace("\n", "").replace("\r", "").replace("\t","")
    if DEBUG:
       print(tab + exp)
    # Eval () and replace result
    while "(" in exp:
        start = exp.rfind("(")
        end = exp.find(")", start)
        evaled = eval_num_expression(exp[start+1:end], tab_cout + 1)
        if (evaled == None):
            return None
        exp = exp[:start] + str(evaled) + exp[end+1:]

    # Tokenize
    tokens = []
    last_num_str = ""
    for c in exp:
        if c in ['+', '-', '*', '/']:
            if last_num_str:
                tokens.append(('int',int(last_num_str), 0))
                last_num_str = ""
            tokens.append(('operator',c, c in ['+', '-'] and 1 or 2))
        elif c.isdigit():
            last_num_str += c
        else:
            return None

    if last_num_str:
        tokens.append(('int',int(last_num_str), 0))
        last_num_str = ""

    if DEBUG:
        print(tokens)

    # Evaluate tokens
    while tokens.__len__() > 1:
        operator_index = -1
        for i, token in enumerate(tokens):
            if token[0] == 'operator' and (operator_index < 0 or tokens[operator_index][2] < token[2]):
                operator_index = i
        if operator_index == -1 or operator_index < 1 or operator_index >= tokens.__len__():
            return None
        
        left_side = tokens[operator_index - 1]
        operator = tokens[operator_index]
        right_side = tokens[operator_index + 1]

        evaled = eval_tokens(left_side, operator, right_side)
        if (evaled == None):
            return None
        
        tokens[operator_index] = ('int', evaled, 0)
        del tokens[operator_index + 1]
        del tokens[operator_index - 1]

        if DEBUG:
            print(tokens)

    if tokens.__len__() == 1 and tokens[0][0] == 'int':
        return tokens[0][1]
    return None


if __name__ == "__main__":
    input_count = int(input())
    for i in range(input_count):
        exp = input()
        evaled = eval_num_expression(exp)
        if evaled == None:
            print("ERROR")
        else:
            print(evaled)