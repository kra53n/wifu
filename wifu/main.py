from astree import AST
from interpret import interpret


if __name__ == '__main__':
    with open('../examples/ex2.w') as f:
        code = f.read()
    ast = AST(code.split('\n'))
    # print(ast)
    interpret(ast)

    # for func_decl in ast._func_decls:
    #     for arg in func_decl._args:
    #         print(arg)
