import sys
import pathlib

from .astree import AST
from .atree import AT
from .interpret import interpret


def main():
    argv = sys.argv[1:]
    if len(argv) != 1:
        print('Currently only 1 script file is allowed')
        return
    code = pathlib.Path(argv[0]).read_text()
    ast = AST(code.split('\n'))
    at = AT(ast)
    interpret(at)
    


if __name__ == '__main__':
    main()
