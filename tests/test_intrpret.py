from fixtures import *

import wifu


def test_intrpret_say_hello_prog(func_say_hello_prog):
    code = func_say_hello_prog.split('\n')
    ast = wifu.AST(code)
    at = wifu.AT(ast)
    wifu.interpret.interpret(at)


def test_arithmetic_expression(get_arithmetic_expression):
    expr = get_arithmetic_expression()
    print(expr)
