from typing import Any, Type

from atoms import Atom
from utils import notify
from repr import Representable


SPACES = ' ' * 4


# class SyntaxError(Exception):
#     pass


class IndentationProblem(Exception):
    pass


class DoubleColumnDecl:
    def __init__(self, name: str, kind: str, default_val: str):
        pass


def get_double_column_decl_by_line(obj: Type[DoubleColumnDecl], line: str, err_msg: str):
    '''
    return obj with initialized arguments:
        - name: str
        - kind: str
        - default_val: str

    the obj returns by parsing string like `obj : type : val` or some variation
    '''
    kind = ''
    default_val = ''
    columns = line.count(':')
    if columns == 0:
        name = line.strip()
    elif columns == 1:
        column = line.index(':')
        name = line[:column].strip()
        kind = line[column+1:].strip()
    elif columns == 2:
        fst_column = line.index(':')
        snd_column = line.index(':', fst_column+1)
        name = line[:fst_column].strip()
        kind = line[fst_column+1:snd_column].strip()
        default_val = line[snd_column+1:].strip()
    else:
        raise SyntaxError(err_msg)
    return obj(name, kind, default_val)


class StructField(Representable, DoubleColumnDecl):
    def __init__(self, name: str, kind: str, default_val: str):
        self.name = name
        self.kind = kind
        self.default_val = default_val

    def repr(self, indent = 0):
        return SPACES * indent + f'{self.name} : {self.kind or None} : {self.default_val or None}'


class Struct(Representable):
    def __init__(self, name: str, fields: list[StructField]):
        self.name = name
        self.fields = fields

    def repr(self, indent = 0):
        res = SPACES * (indent + 0) + self.name
        if self.fields:
            res += '\n'
            res += '\n'.join(map(lambda x: x.repr(indent+1), self.fields))
        return res


def is_struct(line: str) -> bool:
    return line.strip() == 'struct'


def get_struct_name(code: list[str], line_num: int, base_indent: int) -> (str, int):
    line_num += 1
    if base_indent >= define_line_indent(code[line_num]):
        raise SyntaxError('there is indentation or no struct name declaration problem')
    return code[line_num].strip(), line_num


def get_struct_field_by_line(line: str) -> StructField:
    return get_double_column_decl_by_line(StructField, line, 'syntax error in field declaration')


def get_struct_fields(code: list[str], line_num: int, base_indent: int) -> (list[StructField], int):
    fields: list[StructField] = []
    line_num += 1
    while line_num < len(code) and base_indent < define_line_indent(code[line_num]):
        if is_single_comment(code[line_num]):
            line_num += 1
            continue
        field = get_struct_field_by_line(code[line_num])
        fields.append(field)
        line_num += 1
    return fields, line_num


def parse_struct(code: list[str], line_num: int) -> (Struct, int):
    name, line_num = get_struct_name(code, line_num, define_line_indent(code[line_num]))
    fields, line_num = get_struct_fields(code, line_num, define_line_indent(code[line_num]))
    return Struct(name, fields), line_num


class FuncDeclArg(DoubleColumnDecl):
    def __init__(self, name: str, kind: str, default_val: str):
        '''
        - kind accepts str but then when `AT` is callig it must be transformed
        to reference on some atom
        - default_val accepts str but then when `AT` is calling it must be
        transformed to one of the Atom type.
        '''
        self._name: str = name
        self.kind: str | Atom = kind
        self.default_val: str | Atom = default_val

    def __str__(self):
        return f'FuncDeclArg[name={self._name}, kind={self._kind or None}, default_val={self.default_val or None}]'

    def __repr__(self):
        return self.__str__()


def get_func_decl_arg_by_line(line: str):
    return get_double_column_decl_by_line(FuncDeclArg, line, 'syntax error in arguemnt function declarationn')


class FuncCallArg(Representable):
    def __init__(self, data: str):
        self.data = data
        self.kind: Atom = None

    def repr(self, indent = 0):
        return self.data


class FuncCall(Representable):
    def __init__(self, name: str):
        self._name = name
        self.args = []
        # self._kwargs = [] # TODO(kra53n): implement later

    def add(self, arg):
        self.args.append(arg)

    def pop(self) -> Any:
        if not len(self.args):
            return None
        elem = self.args[-1]
        self.args = self.args[:-1]
        return elem

    def __str__(self):
        return f'FuncCall[{self._name}, args {self.args}]'

    def __repr__(self):
        return self.__str__()

    def repr(self, indent: int = 0):
        res = SPACES * (indent + 0) + self._name + '\n'
        for arg in self.args:
            if isinstance(arg, FuncCall):
                res += arg.repr(indent+1)
            else:
                res += SPACES * (indent+1) + arg.repr()
            res += '\n'
        if len(res):
            return res[:-1]
        return res


class FuncDecl(Representable):
    def __init__(self, name: str, start: int, args: list[FuncDeclArg], body: list[FuncCall]):
        self.name: str = name
        self.start: int = start
        self.args: list[FuncDeclArg] = args
        self.body: list[FuncCall] = body

    def __str__(self):
        return f'Func[{self.name}, start {self.start}, args {len(self.args)}]'

    def __repr__(self):
        return self.__str__()

    def repr(self, indent = 0):
        return self.__str__()


def is_func_call(line: str) -> bool:
    if len(line) == 0 or line.startswith(' ') or line.startswith('\t'):
        return False
    if 'func' not in line:
        return True
    s = line[line.index('func')+len('func'):]
    spaces = s.count(' ')
    tabs = s.count('\t')
    return len(s) and (len(s) - spaces - tabs > 0)


def is_func_decl(line: str) -> bool:
    return line.strip() == 'func'


def define_line_indent(line: str) -> int:
    if not len(line):
        return 0
    i = 0
    while line[i] in (' ', '\t'):
        i += 1
    return i


def skip_empty_lines(code: list[str], line_num: int) -> int:
    while not code[line_num].strip():
        line_num += 1
    return line_num


def get_func_decl_name(code: list[str], line_num: int, base_indent: int) -> (str, int):
    line_num += 1
    line_num = skip_empty_lines(code, line_num)
    func_name = code[line_num].strip()
    if base_indent >= define_line_indent(code[line_num]):
        raise IndentationProblem('problem with indentation of function name')
    return func_name, line_num


def get_func_decl_args(code: list[str], line_num: int, base_indent: int) -> (list[FuncDeclArg], int):
    line_num += 1
    line_num = skip_empty_lines(code, line_num)
    args: FuncDeclArg = []
    indent = define_line_indent(code[line_num])
    while indent > base_indent:
        args.append(get_func_decl_arg_by_line(code[line_num]))
        line_num += 1
        next_indent = define_line_indent(code[line_num])
        if next_indent > indent:
            raise IndentationProblem()
        indent = next_indent
    return args, line_num


def get_func_decl_body(code: list[str], line_num: int, base_indent: int) -> (list[FuncCall], int):
    line_num = skip_empty_lines(code, line_num)
    body: list[FuncCall] = []
    while (line_num < len(code) and
           (indent := define_line_indent(code[line_num])) and
           indent > base_indent):
        func_call, line_num = parse_func_call(code, line_num)
        body.append(func_call)
        line_num += 1
    return body, line_num


def parse_func_call(code: list[str], line_num: int) -> (FuncCall, int):
    func_name = code[line_num].strip()
    func_call = FuncCall(func_name)

    base_indent = define_line_indent(code[line_num])
    indent = base_indent
    while line_num + 1 < len(code):
        line_num += 1
        line_indent = define_line_indent(code[line_num])
        if indent == base_indent:
            if line_indent > base_indent:
                indent = line_indent
            else:
                line_num -= 1
                break

        if line_indent == indent:
            func_call.add(FuncCallArg(code[line_num].strip()))
        elif line_indent > indent:
            func_call.pop()
            inner_func_call, line_num = parse_func_call(code, line_num-1)
            func_call.add(inner_func_call)
        else:
            line_num -= 1
            break
    return func_call, line_num


def parse_func_decl(code: list[str], line_num: int) -> (FuncDecl, int):
    start = line_num
    indent = define_line_indent(code[line_num])
    func_name, line_num = get_func_decl_name(code, line_num, indent)
    args, line_num = get_func_decl_args(code, line_num, define_line_indent(code[line_num]))
    body, line_num = get_func_decl_body(code, line_num, indent)
    return FuncDecl(func_name, start, args, body), line_num


def is_single_comment(line: str) -> bool:
    line = line.strip()
    return len(line) and (line[0] == '#')


def is_multiline_comment(line: str) -> bool:
    line = line.strip()
    return ((len(line) >= 3 and
             (line[:3].count("'") == 3 or
              line[:3].count('"') == 3)))


def ignore_multiline_comment(code: list[str], line_num: int) -> (None, int):
    comment_signature = code[line_num].strip()[:3]
    while line_num + 1 < len(code):
        line_num += 1
        line = code[line_num]
        if len(line) and line.find(comment_signature) != -1:
            return None, line_num
    return None, line_num


class AST:
    def __init__(self, code: list[str]):
        self.structs: list[Struct] = []
        self.func_decls: list[FuncDecl] = []
        self.func_calls: list[FuncCall] = []
        self._build(code)

    def _build(self, code: list[str]):
        line_num = 0
        while line_num < len(code):
            line = code[line_num]
            if is_single_comment(line):
                pass
            elif is_multiline_comment(line):
                _, line_num = ignore_multiline_comment(code, line_num)
            elif is_struct(line):
                struct, line_num = parse_struct(code, line_num)
                self.structs.append(struct)
            elif is_func_decl(line):
                func_decl, line_num = parse_func_decl(code, line_num)
                self.func_decls.append(func_decl)
            elif is_func_call(line):
                func_call, line_num = parse_func_call(code, line_num)
                self.func_calls.append(func_call)
            line_num += 1

    def __repr__(self):
        names = 'stucts', 'func decls', 'func calls'
        funcs = self.repr_structs, self.repr_func_decls, self.repr_func_calls
        return '\n'.join(f'\n{notify("*", 30, name.capitalize())}\n{func()}'
                         for name, func in zip(names, funcs))
    
    def repr_structs(self):
        return '\n\n'.join(map(lambda x: x.repr(), self.structs))

    def repr_func_decls(self):
        return '\n'.join(map(lambda x: x.repr(), self.func_decls))

    def repr_func_calls(self):
        return '\n'.join(map(lambda x: x.repr(), self.func_calls))
