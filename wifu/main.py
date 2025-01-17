from astree import AST


if __name__ == '__main__':
    with open('examples/ex3.w') as f:
        code = f.read()
    ast = AST(code.split('\n'))
    # ast.print()

    for func_decl in ast._func_decls:
        for arg in func_decl._args:
            print(arg)
