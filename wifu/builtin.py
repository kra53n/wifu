from typing import (
    Iterable,
)

from .import astree 


class Func:
    def __init__(self, func):
        self.func = func

    def exec(self, func_call: astree.FuncCall):
        self.func(func_call)


def _print(func_call: astree.FuncCall):
    args: Iterable[astree.FuncCallArg] = func_call.args
    for arg in args:
        print(arg.kind.data)


funcs: dict[str, Func] = {
    'print': Func(_print),
}
