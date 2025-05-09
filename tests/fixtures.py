from typing import (
    Callable,
    Generator,
)


import pytest


@pytest.fixture
def func_say_hello_prog() -> str:
    #     Problems:
    # 1. `\n`
    return (
'''
say hello

func
    say hello
    print
        'hello world'
        3.14
        'pez'
''')


@pytest.fixture
def get_arithmetic_expressions() -> Callable[None, Generator[tuple[str, str], None, None]]:
    def wrapper():
        expr = (
'''
%s
    12
    13
''')
        for op in (*'+-*/%^', '++', '**'):
            yield expr % op
        return
    return wrapper


@pytest.fixture
def get_arithmetic_expressions_only_with_double_sign() -> Callable[None, Generator[tuple[str, str], None, None]]:
    def wrapper():
        expr = (
'''
%s
    12
    13
    14
    15
    16
    17
    18
    19
    20
''')
        for op in ('++', '**'):
            yield expr % op
        return
    return wrapper
