from typing import (
    Optional,
)

from .atree import AT
from .astree import FuncCall, FuncDecl
from . import builtin


def func_in_builtin_or_declared(
    func_call: FuncCall,
        func_decls: list[FuncDecl]
) -> Optional[FuncDecl | builtin.Func]:
    if func_call._name in builtin.funcs:
        return builtin.funcs[func_call._name]
    for func_decl in func_decls:
        if func_decl.name == func_call._name:
            return func_decl
    return


def find_decl(func_call: FuncCall, func_decls: list[FuncDecl]) -> FuncDecl:
    func_decl = func_in_builtin_or_declared(func_call, func_decls)
    if not func_decl:
        return Exception(f'function {func_call._name} was not declared')
    return func_decl


def call(func_call: FuncCall, decls: list[FuncDecl]):
    decl = find_decl(func_call, decls)

    if isinstance(decl, builtin.Func):
        return decl.exec(func_call)

    # i guess we should make variables from args that then we can use in a function

    # im not sure what expression means, maybe i should use statement word
    for expr in decl.body:
        if isinstance(expr, FuncCall):
            return call(expr, decls)


def interpret(at: AT):
    for func_call in at.func_calls:
        call(func_call, at.func_decls)
        # if not can_call_func(func_call, at.func_calls):
        #     raise Exception(f'function {func_call} does not exist')
        # assert func_call in at.func_decls
        # print(func_call)
    # for func_decl in at.func_decls:
    #     print(func_decl)
