from atoms import Atom, Str, Char, Int, Float, Fraction, Generic
from astree import AST, FuncCall, FuncCallArg, FuncDecl, FuncDeclArg


def str_to_atom_ref(kind: str):
    return {
        'str': Str,
        'chr': Char,
        'int': Int,
        'float': Float,
        'fract': Fraction,
    }[kind]


def looks_like_str(data: str) -> bool:
    return (len(data) > 2 and data[0] == '"' or
            len(data) > 3 and data[0] == "'")


def looks_like_char(data: str) -> bool:
    return len(data) == 3 and data[0] in ('"', "'")


def looks_like_num(data: str) -> bool:
    fst = data[0]
    snd = data[1] if len(data) > 1 else None
    return (fst.isdigit() or
            ((fst == '.' or fst == '-') and
             snd.isdigit()))


def get_atom(data: str) -> Atom:
    for looks_like_something, approptiate_atom in ((looks_like_str, get_as_str_atom),
                                                   (looks_like_num, get_as_num_atom),
                                                   (looks_like_char, get_as_char_atom)):
        if looks_like_something(data):
            return approptiate_atom(data)


def get_as_char_atom(data: str) -> Atom:
    return Char(data[1])


def get_as_str_atom(data: str) -> Atom:
    for i, c in enumerate(data[1:]):
        if c == data[0]:
            # print(Str(data[1:i+1]))
            return Str(data[1:i+1])
    raise SyntaxError('string literal should be closed with \' or " in the same line')


def get_as_num_atom(data: str) -> Atom:
    is_signed = False
    is_mantissa = False
    is_fraction = False
    left_num, right_num = '', ''
    for i, v in enumerate(data):
        if v.isdigit():
            if is_mantissa or is_fraction:
                right_num += v
            else:
                left_num += v
        elif v == '-':
            if is_signed:
                raise SyntaxError('`-` should be only one in the num')
            else:
                is_signed = True
        elif v == '.':
            if is_mantissa:
                raise SyntaxError('`.` should be only one in the float num')
            else:
                is_mantissa = True
        elif v == '/':
            if is_fraction:
                raise SyntaxError('`/` should be only one in the fraction')
            else:
                is_fraction = True
    if is_mantissa and is_fraction:
        raise SyntaxError('num can be only be float or fraction, not mixed')
    left_num = ('-' if is_signed else '') + left_num
    if is_mantissa:
        return Float(left_num, right_num)
    elif is_fraction:
        return Fraction(left_num, right_num)
    return Int(left_num)


class AT:
    def __init__(self, ast: AST):
        # self.structs
        self.func_decls: list[FuncDecl] = self._process_func_decls_of_ast(ast)
        self.func_calls: list[FuncCall] = self._process_func_calls_of_ast(ast)
        print('nani')

    # NOTE(kra53n): actually i dont think that `process` is a good word for
    # this and similur actions
    #
    # subject consists with group of atoms
    def process_subject(self, subject):
        if isinstance(subject, FuncCall):
            for func_call_arg in subject.args:
                self.process_subject(func_call_arg)
        elif isinstance(subject, FuncCallArg):
            subject.kind = get_atom(subject.data)
        elif isinstance(subject, FuncDecl):
            for func_decl_arg in subject.args:
                self.process_subject(func_decl_arg)
        elif isinstance(subject, FuncDeclArg):
            subject.kind = str_to_atom_ref(subject.kind) if subject.kind else Generic
            if subject.default_val:
                subject.default_val = get_atom(subject.default_val)
        return subject
    
    def _process_func_calls_of_ast(self, ast: AST):
        return [self.process_subject(fc) for fc in ast.func_calls]

    def _process_func_decls_of_ast(self, ast: AST):
        return [self.process_subject(fc) for fc in ast.func_decls]
