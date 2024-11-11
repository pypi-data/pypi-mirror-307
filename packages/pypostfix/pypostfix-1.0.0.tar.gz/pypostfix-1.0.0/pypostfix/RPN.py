def rpn_is_valid(RPN_expression: str, sep: str = ' ') -> bool:
    """This function takes as input an expression written in Reverse Polish Notation (RPN) and a separator character that delineates each element in the expression. It interprets the operators + for addition, - for subtraction, * for multiplication, / for division, ^ for exponentiation, dup to duplicate the last item on the stack, swap to exchange the last two items, sqrt for the square root, sin for the sine function, cos for the cosine function, and tan for the tangent function.
    It returns if the expression is valid."""
    stack = []
    
    tokens = RPN_expression.split(sep)
    
    for token in tokens:
        if token.isdigit() or (token.replace('.', '', 1).isdigit() and token.count('.') < 2):
            stack.append(token)

        elif token in ['+', '-', '*', '/', '^', 'dup', 'swap', 'sqrt', 'sin', 'cos', 'tan']:
            if token in ['+', '-', '*', '/', '^']:
                if len(stack) < 2:
                    return False
                if token == "/" and stack[-1] == "0":
                    return False
                stack.pop()

            elif token in ['sin', 'cos', 'tan', 'sqrt']:
                if len(stack) < 1:
                    return False
                if token == 'sqrt':
                    val = float(stack[-1])
                    if val < 0:
                        return False
                    
            elif token == "swap":
                if len(stack) < 2:
                    return False
                    
            elif token == "dup":
                stack.append(stack[-1])
                
            else:
                return False
            
        else:
            return False

    return len(stack) == 1


###################################


def calc_rpn(RPN_expression: str, sep: str = ' ') -> float:
    """This function takes as input an expression written in Reverse Polish Notation (RPN) and a separator character that delineates each element in the expression. It interprets the operators + for addition, - for subtraction, * for multiplication, / for division, ^ for exponentiation, dup to duplicate the last item on the stack, swap to exchange the last two items, sqrt for the square root, sin for the sine function, cos for the cosine function, and tan for the tangent function.
    It returns the result of the expression. """
    if rpn_is_valid(RPN_expression):
        import math

        tokens = RPN_expression.split(sep)

        while len(tokens) > 1:
            for i, token in enumerate(tokens):
                if token in ["+", "-", "*", "/", "^"]:
                    if token == "+":
                        tokens[i-2] = str(float(tokens[i - 2]) + float(tokens[i - 1]))
                    elif token == "-":
                        tokens[i-2] = str(float(tokens[i - 2]) - float(tokens[i - 1]))
                    elif token == "*":
                        tokens[i-2] = str(float(tokens[i - 2]) * float(tokens[i - 1]))
                    elif token == "/":
                        tokens[i-2] = str(float(tokens[i - 2]) / float(tokens[i - 1]))
                    elif token == "^":
                        tokens[i-2] = str(float(tokens[i - 2]) ** float(tokens[i - 1]))
                    tokens.pop(i)
                    tokens.pop(i-1)
                    break
                        

                elif token in ["sin", "cos", "tan", "sqrt", "swap"]:
                    if token == "sin":
                        tokens[i-1] = str(math.sin(float(tokens[i - 1])))
                    elif token == "cos":
                        tokens[i-1] = str(math.cos(float(tokens[i - 1])))
                    elif token == "tan":
                        tokens[i-1] = str(math.tan(float(tokens[i - 1])))
                    elif token == "sqrt":
                        tokens[i-1] = str(math.sqrt(float(tokens[i - 1])))
                    elif token == "swap":
                        temp = tokens[i-1]
                        tokens[i-1] = tokens[i-2]
                        tokens[i-2] = temp
                    
                    tokens.pop(i)
                    break
                
                elif token == "dup":
                    tokens[i] = tokens[i-1]
                    break
                    

        return tokens[0]
            
    raise ValueError("Invalid postfix (RPN) expression")


###################################


def rpn_to_infix(expression: str, sep: str = " ") -> str:
    """This function takes as input an expression written in Reverse Polish Notation (RPN) and a separator character that delineates each element in the expression. It interprets the operators + for addition, - for subtraction, * for multiplication, / for division, ^ for exponentiation, dup to duplicate the last item on the stack, swap to exchange the last two items, sqrt for the square root, sin for the sine function, cos for the cosine function, and tan for the tangent function.
    It returns an infix expression."""

    if rpn_is_valid(expression):

        stack = []
        for token in expression.split(sep): # 2 arguments operations
            if token in ["+", "-", "*", "/", "^", "swap"]:
                b = stack.pop()
                a = stack.pop()
                if token == "+":
                    stack.append(f"({a} + {b})")
                elif token == "-":
                    stack.append(f"({a} - {b})")
                elif token == "*":
                    stack.append(f"({a} * {b})")
                elif token == "/":
                    stack.append(f"({a} / {b})")
                elif token == "^":
                    stack.append(f"({a} ^ {b})")
                elif token == "swap":
                    stack.append(b)
                    stack.append(a)

            elif token in ["sin", "cos", "tan", "sqrt", "dup"]: # 1 argument operations
                a = stack.pop()
                if token == "sin":
                    stack.append(f"sin({a})")
                elif token == "cos":
                    stack.append(f"cos({a})")
                elif token == "tan":
                    stack.append(f"tan({a})")
                elif token == "sqrt":
                    stack.append(f"sqrt({a})")
                elif token == "dup":
                    stack.append(a)
                    stack.append(a)

            else:
                stack.append(token)
        return stack[0]
    
    raise ValueError("Invalid postfix (RPN) expression")


###################################


def infix_to_rpn(infix_expression: str, sep: str = ' ') -> str:
    """This function takes as input an infix expression and a separator character that will delineates each element in the output Reverse Polish Notation (RPN) expression. It interprets the operators + for addition, - for subtraction, * for multiplication, / for division, ^ for exponentiation, dup to duplicate the last item on the stack, swap to exchange the last two items, sqrt for the square root, sin for the sine function, cos for the cosine function, and tan for the tangent function.
    It returns the result of the Reverse Polish Notation (RPN) expression. """
    import re

    priorite = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2,
        '^': 3,
        'sin': 4,
        'cos': 4,
        'tan': 4,
        'sqrt': 4
    }

    pile = []
    sortie = []
    
    tokens = re.findall(r'\d+\.\d+|\d+|[a-zA-Z]+|[+\-*/^()]', infix_expression)

    for element in tokens:
        if element.isdigit() or re.match(r'\d+\.\d+', element):
            sortie.append(element)
        elif element in priorite:
            while (pile and pile[-1] != '(' and
                   priorite.get(pile[-1], 0) >= priorite[element]):
                sortie.append(pile.pop())
            pile.append(element)
        elif element == '(':
            pile.append(element)
        elif element == ')':
            while pile and pile[-1] != '(':
                sortie.append(pile.pop())
            pile.pop()

    while pile:
        sortie.append(pile.pop())

    return sep.join(sortie)