from typing import (
    Iterable,
)

from .import astree 
from .import atom


class Func:
    def __init__(self, func):
        self.func = func

    def exec(self, func_call: astree.FuncCall):
        return self.func(func_call)


def _print(func_call: astree.FuncCall):
    args: Iterable[astree.FuncCallArg] = func_call.args
    for arg in args:
        # NOTE(kra53n, 20260126) we should to operate statements and expressions.
        # Here we should to print expression. So maybe we can avoid this, but we faced with fact
        # that we can't just to get attribute from atom and print it. It is not working
        # when we whant to print what other function evaluates.

        # NOTE(kra53n, 20260126) it would be easier to make if we will print an evaluated expressions
        # like 1 + 2 * 2 and etc.
        print(arg)
        print(arg.kind.format_data())


def _plus(func_call: astree.FuncCall):
    args: Iterable[astree.FuncCallArg] = func_call.args
    assert len(args) == 2
    fst, snd = args
    assert atom.equals(fst.kind, snd.kind)
    return fst.kind.data + snd.kind.data


def _minus(func_call: astree.FuncCall):
    args: Iterable[astree.FuncCallArg] = func_call.args
    assert len(args) == 2
    fst, snd = args
    assert atom.equals(fst.kind, snd.kind)
    return fst.kind.data - snd.kind.data


def _asterisk(func_call: astree.FuncCall):
    args: Iterable[astree.FuncCallArg] = func_call.args
    assert len(args) == 2
    fst, snd = args
    assert atom.equals(fst.kind, snd.kind)
    return fst.kind.data * snd.kind.data


def _divide(func_call: astree.FuncCall):
    args: Iterable[astree.FuncCallArg] = func_call.args
    assert len(args) == 2
    fst, snd = args
    assert atom.equals(fst.kind, snd.kind)
    return fst.kind.data / snd.kind.data


def _percent(func_call: astree.FuncCall):
    args: Iterable[astree.FuncCallArg] = func_call.args
    assert len(args) == 2
    fst, snd = args
    assert atom.equals(fst.kind, snd.kind)
    return fst.kind.data % snd.kind.data


def _circumflex(func_call: astree.FuncCall):
    args: Iterable[astree.FuncCallArg] = func_call.args
    assert len(args) == 2
    fst, snd = args
    assert atom.equals(fst.kind, snd.kind)
    return fst.kind.data ** snd.kind.data


def _plusplus(func_call: astree.FuncCall):
    args: Iterable[astree.FuncCallArg] = func_call.args
    assert len(args) > 1
    kind = args[0].kind
    kinds = tuple(map(lambda arg: arg.kind, args))
    assert all(map(lambda k: atom.equals(kind, k), kinds))
    res = 0
    for v in map(lambda kind: kind.data, kinds):
        res += v
    return kind.__class__(res)


def _asteriskasterisk(func_call: astree.FuncCall):
    args: Iterable[astree.FuncCallArg] = func_call.args
    assert len(args) > 1
    kind = args[0].kind
    kinds = tuple(map(lambda arg: arg.kind, args))
    assert all(map(lambda k: atom.equals(kind, k), kinds))
    res = 1
    for v in map(lambda kind: kind.data, kinds):
        res *= v
    return res


funcs: dict[str, Func] = {
    'print': Func(_print),
    '+': Func(_plus),
    '-': Func(_minus),
    '*': Func(_asterisk),
    '/': Func(_divide),
    '%': Func(_percent),
    '^': Func(_circumflex),
    '++': Func(_plusplus),
    '**': Func(_asteriskasterisk),
}
