'''
The base types of the language
'''

class Atom:
    def __init__(self, data: str):
        self.data = data

    def __repr__(self):
        return f'{self.__class__.__name__}[{self.data}]'


class Str(Atom):
    pass


class Char(Atom):
    pass


class Int(Atom):
    def __init__(self, data: str):
        self.data = int(data)


class Float(Atom):
    def __init__(self, left: str, right: str):
        self.data = float(left + '.' + right)


class Fraction(Atom):
    def __init__(self, numerator: str, denominator: str):
        self.numerator = int(numerator)
        self.denominator = int(denominator)


class Generic(Atom):
    pass
