'''
The base types of the language
'''

import typing


class Atom:
    def __init__(self, data: str):
        self.data = data

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}[{self.data}]'

    def format_data(self) -> str:
        '''
        Return data that can be printed using print wifu function.
        
        The most atoms could be presented only with on variable (self.data).
        But there is some atoms that needs to have more variables like Fraction.
        '''
        return self.data


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

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}[{self.numerator}/{self.denominator}]'

    def format_data(self) -> str:
        return f'{self.numerator}/{self.denominator}'


class Generic(Atom):
    pass


def equals(atom1: Atom, atom2: Atom):
    return atom1.__class__.__name__ == atom2.__class__.__name__
