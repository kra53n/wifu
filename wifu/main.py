from ast import AST


if __name__ == '__main__':
    with open('../examples/ex1.w') as f:
        code = f.read()
    ast = AST(code.split('\n'))
    ast.print()
