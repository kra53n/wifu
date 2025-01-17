from astree import AST, FuncCall, FuncCallArg


class Atom:
    def __init__(self, data: str):
        pass


class Str(Atom):
    def __init__(self, data: str):
        self.data = data


class Char(Atom):
    def __init__(self, data: str):
        self.data = data


class Int(Atom):
    def __init__(self, data: int):
        self.data = data


class Float(Atom):
    def __init__(self, data: float):
        self.data = data


def get_atom(data: str) -> Atom:
    fst = data[0]
    if fst in ("'", '"'):
        if len(data) == 1 and fst == "'":
            return get_as_char_atom(data)
        return get_as_str_atom(data)
    if fst.isdigit() or fst == '.':
        return get_as_num(data)


def get_as_char_atom(data: str):
    pass


def get_as_str_atom(data: str):
    pass


def get_as_num_atom(data: str):
    pass


class AT:
    def __init__(self, ast: AST):
        # self.structs
        # self.func_decls
        self.func_calls = self._process_func_calls_of_ast(ast)

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
        return subject
    
    def _process_func_calls_of_ast(self, ast):
        return [self._process_subject(fc) for fc in ast.func_calls]