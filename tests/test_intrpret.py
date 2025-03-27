from fixtures import *

import wifu


def test_intrpret_say_hello_prog(func_say_hello_prog):
    code = func_say_hello_prog.split('\n')
    ast = wifu.AST(code)
    at = wifu.AT(ast)
    wifu.interpret.interpret(at)
