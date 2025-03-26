from .astree import AST
from .atree import AT
from .interpret import interpret


if __name__ == '__main__':
    with open('examples/ex3.w') as f:
        code = f.read()
    ast = AST(code.split('\n'))
    at = AT(ast)
    from pprint import pprint
    print(at)
    # pprint(dir(at))
    print(at.func_calls)
    print(at.func_decls)


    # print(ast)
    # interpret(ast)

    # for func_decl in ast._func_decls:
    #     for arg in func_decl._args:
    #         print(arg)
