from fixtures import *

import wifu


def test_intrpret_say_hello_prog(func_say_hello_prog):
    code = func_say_hello_prog.split('\n')
    ast = wifu.AST(code)
    at = wifu.AT(ast)
    wifu.interpret.interpret(at)


def test_arithmetic_expression(get_arithmetic_expressions):
    for expr in get_arithmetic_expressions():
        code = expr.split('\n')
        ast = wifu.AST(code)
        at = wifu.AT(ast)
        expr_in_str = f"{code[2].strip()} {code[1]} {code[3].strip()}"
        print(f":: arithmetic expr res {expr_in_str}: {wifu.interpret.call(at.func_calls[0], at.func_decls)}") 


def test_arithmetic_expression_only_with_double_sign(get_arithmetic_expressions_only_with_double_sign):
    for expr in get_arithmetic_expressions_only_with_double_sign():
        code = expr.split('\n')
        ast = wifu.AST(code)
        at = wifu.AT(ast)
        expr_in_str = f"{code[2].strip()} {code[1]} {code[3].strip()}"
        print(f":: arithmetic expr res {expr_in_str}: {wifu.interpret.call(at.func_calls[0], at.func_decls)}") 
