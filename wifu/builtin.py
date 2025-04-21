from typing import (
    Iterable,
)

from .import astree 
from .import atoms


class Func:
    def __init__(self, func):
        self.func = func

    def exec(self, func_call: astree.FuncCall):
        return self.func(func_call)


def _print(func_call: astree.FuncCall):
    args: Iterable[astree.FuncCallArg] = func_call.args
    for arg in args:
        print(arg.kind.data)


def _plus(func_call: astree.FuncCall):
    args: Iterable[astree.FuncCallArg] = func_call.args
    assert len(args) == 2
    fst, snd = args
    assert atoms.equals(fst.kind, snd.kind)
    return fst.kind.data + snd.kind.data


def _minus(func_call: astree.FuncCall):
    args: Iterable[astree.FuncCallArg] = func_call.args
    assert len(args) == 2
    fst, snd = args
    assert atoms.equals(fst.kind, snd.kind)
    return fst.kind.data - snd.kind.data


def _asterisk(func_call: astree.FuncCall):
    args: Iterable[astree.FuncCallArg] = func_call.args
    assert len(args) == 2
    fst, snd = args
    assert atoms.equals(fst.kind, snd.kind)
    return fst.kind.data * snd.kind.data


def _divide(func_call: astree.FuncCall):
    args: Iterable[astree.FuncCallArg] = func_call.args
    assert len(args) == 2
    fst, snd = args
    assert atoms.equals(fst.kind, snd.kind)
    return fst.kind.data / snd.kind.data


def _percent(func_call: astree.FuncCall):
    args: Iterable[astree.FuncCallArg] = func_call.args
    assert len(args) == 2
    fst, snd = args
    assert atoms.equals(fst.kind, snd.kind)
    return fst.kind.data % snd.kind.data


def _circumflex(func_call: astree.FuncCall):
    args: Iterable[astree.FuncCallArg] = func_call.args
    assert len(args) == 2
    fst, snd = args
    assert atoms.equals(fst.kind, snd.kind)
    return fst.kind.data ** snd.kind.data


def _plusplus(func_call: astree.FuncCall):
    args: Iterable[astree.FuncCallArg] = func_call.args
    assert len(args) > 1
    kind = args[0].kind
    kinds = tuple(map(lambda arg: arg.kind, args))
    assert all(map(lambda k: atoms.equals(kind, k), kinds))
    res = 0
    for v in map(lambda kind: kind.data, kinds):
        res += v
    return res


def _asteriskasterisk(func_call: astree.FuncCall):
    args: Iterable[astree.FuncCallArg] = func_call.args
    assert len(args) > 1
    kind = args[0].kind
    kinds = tuple(map(lambda arg: arg.kind, args))
    assert all(map(lambda k: atoms.equals(kind, k), kinds))
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
