'''
Test module implies to use pytest or something simular that can work
with `assert` Python statement.
'''


from wifu import (
    atom,
    atree,
)


class TestGetAsNumAtom:
    def test_signed_int(self):
        a = atree.get_as_num_atom('-12')
        assert isinstance(a, atom.Int)
        assert a.data == -12

    def test_unsigned_int(self):
        a = atree.get_as_num_atom('12')
        assert isinstance(a, atom.Int)
        assert a.data == 12

    def test_signed_float(self):
        a = atree.get_as_num_atom('-12.12')
        assert isinstance(a, atom.Float)
        assert a.data == -12.12

    def test_unsigned_float(self):
        a = atree.get_as_num_atom('12.12')
        assert isinstance(a, atom.Float)
        assert a.data == 12.12

    def test_signed_fraction(self):
        a = atree.get_as_num_atom('-1/2')
        assert isinstance(a, atom.Fraction)
        assert a.numerator == -1
        assert a.denominator == 2

    def test_unsigned_fration(self):
        a = atree.get_as_num_atom('1/2')
        assert isinstance(a, atom.Fraction)
        assert a.numerator == 1
        assert a.denominator == 2
