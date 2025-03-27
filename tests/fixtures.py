import pytest


@pytest.fixture
def func_say_hello_prog() -> str:
    #     Problems:
    # 1. `\n`
    # 2. Several args
    return (
'''
say hello

func
    say hello
    print
        'hello world'
''')
