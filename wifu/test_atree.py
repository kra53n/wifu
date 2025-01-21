'''
Test module implies to use pytest or something simular that can work
with `assert` Python statement.
'''


from atree import *


class TestGetAsNumAtom:
    def test_signed_int(self):
        atom = get_as_num_atom('-12')
        assert isinstance(atom, Int)
        assert atom.data == -12

    def test_unsigned_int(self):
        atom = get_as_num_atom('12')
        assert isinstance(atom, Int)
        assert atom.data == 12

    def test_signed_float(self):
        atom = get_as_num_atom('-12.12')
        assert isinstance(atom, Float)
        assert atom.data == -12.12

    def test_unsigned_float(self):
        atom = get_as_num_atom('12.12')
        assert isinstance(atom, Float)
        assert atom.data == 12.12

    def test_signed_fraction(self):
        atom = get_as_num_atom('-1/2')
        assert isinstance(atom, Fraction)
        assert atom.numerator == -1
        assert atom.denominator == 2

    def test_unsigned_fration(self):
        atom = get_as_num_atom('1/2')
        assert isinstance(atom, Fraction)
        assert atom.numerator == 1
        assert atom.denominator == 2
