'''
The base types of the language
'''

import typing


class Atom:
    def __init__(self, data: str):
        self.data = data

    def __repr__(self):
        return f'{self.__class__.__name__}[{self.data}]'


class Str(Atom):
    pass


class Char(Atom):
    pass


class Callculable(Atom):
    def __add__(self, atom: typing.Self):
        return self.__class__(self.data + atom.data)


class Int(Callculable):
    def __init__(self, data: str):
        self.data = int(data)


class Float(Callculable):
    def __init__(self, left: str, right: str):
        self.data = float(left + '.' + right)


class Fraction(Callculable):
    def __init__(self, numerator: str, denominator: str):
        self.numerator = int(numerator)
        self.denominator = int(denominator)


class Generic(Atom):
    pass


def equals(atom1: Atom, atom2: Atom):
    return atom1.__class__.__name__ == atom2.__class__.__name__
