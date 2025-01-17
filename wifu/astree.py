from typing import Any, Union

from utils import notify


class SyntaxError(Exception):
    pass


class IndentationProblem(Exception):
    pass


class FuncDeclArg:
    def __init__(self, name: str, kind: str, default_val: str):
        self._name = name
        self._kind = kind
        self._default_val = default_val

    def __str__(self):
        return f'FuncDeclArg[name={self._name}, kind={self._kind or None}, default_val={self._default_val or None}]'

    def __repr__(self):
        return self.__str__()


def get_func_decl_arg_by_line(line: str):
    name = ''
    kind = ''
    default_val = ''
    columns = line.count(':')
    if columns == 0:
        name = line.strip()
    elif columns == 2:
        fst_column = line.index(':')
        snd_column = line.index(':', fst_column+1)
        name = line[:fst_column].strip()
        kind = line[fst_column+1:snd_column].strip()
        default_val = line[snd_column+1:].strip()
    else:
        raise SyntaxError('syntax error in function declarationn')
    return FuncDeclArg(name, kind, default_val)


class FuncCall:
    def __init__(self, name: str):
        self._name = name
        self._args = []
        self._kwargs = []

    def add(self, arg):
        self._args.append(arg)

    def pop(self) -> Any:
        if not len(self._args):
            return None
        elem = self._args[-1]
        self._args = self._args[:-1]
        return elem

    def __str__(self):
        return f'FuncCall[{self._name}, args {self._args}]'

    def __repr__(self):
        return self.__str__()

    def repr_as_tree(self, indent: int = 0):
        res = ''
        spaces = ' ' * 4
        res += spaces * (indent + 0) + self._name + '\n'
        for arg in self._args:
            if isinstance(arg, FuncCall):
                res += arg.repr_as_tree(indent+1)
            else:
                res += spaces * (indent+1) + arg
            res += '\n'
        if len(res):
            return res[:-1]
        return res


class FuncDecl:
    def __init__(self, name: str, start: int, args: list[FuncDeclArg], body: list[FuncCall]):
        self._name = name
        self._start = start
        self._args = args
        self._body = body

    def __str__(self):
        return f'Func[{self._name}, start {self._start}, args {len(self._args)}]'

    def __repr__(self):
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


def get_func_decl_name(code: list[str], line_num: int, base_indent: int) -> Union[str, int]:
    line_num += 1
    line_num = skip_empty_lines(code, line_num)
    func_name = code[line_num].strip()
    if base_indent >= define_line_indent(code[line_num]):
        raise IndentationProblem('problem with indentation of function name')
    return func_name, line_num


def get_func_decl_args(code: list[str], line_num: int, base_indent: int) -> Union[list[FuncDeclArg], int]:
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


def get_func_decl_body(code: list[str], line_num: int, base_indent: int) -> Union[list[FuncCall], int]:
    line_num = skip_empty_lines(code, line_num)
    body: list[FuncCall] = []
    while (line_num < len(code) and
           (indent := define_line_indent(code[line_num])) and
           indent > base_indent):
        func_call, line_num = parse_func_call(code, line_num)
        body.append(func_call)
        line_num += 1
    return body, line_num


def parse_func_call(code: list[str], line_num: int) -> Union[FuncCall, int]:
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
            func_call.add(code[line_num].strip())
        elif line_indent > indent:
            func_call.pop()
            inner_func_call, line_num = parse_func_call(code, line_num-1)
            func_call.add(inner_func_call)
        else:
            line_num -= 1
            break
    return func_call, line_num


def parse_func_decl(code: list[str], line_num: int) -> Union[FuncDecl, int]:
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


def ignore_multiline_comment(code: list[str], line_num: int) -> Union[None, int]:
    comment_signature = code[line_num].strip()[:3]
    while line_num + 1 < len(code):
        line_num += 1
        line = code[line_num]
        if len(line) and line.find(comment_signature) != -1:
            return None, line_num
    return None, line_num


class AST:
    def __init__(self, code: list[str]):
        self._func_calls: list[FuncCall] = []
        self._func_decls: list[FuncDecl] = []
        self.build(code)

    def build(self, code: list[str]):
        line_num = 0
        while line_num < len(code):
            line = code[line_num]
            if is_single_comment(line):
                pass
            elif is_multiline_comment(line):
                _, line_num = ignore_multiline_comment(code, line_num)
            elif is_func_call(line):
                func_call, line_num = parse_func_call(code, line_num)
                self._func_calls.append(func_call)
            elif is_func_decl(line):
                func_decl, line_num = parse_func_decl(code, line_num)
                self._func_decls.append(func_decl)
            line_num += 1

    def print(self):
        names = 'funcs', 'func calls'
        funcs = self.print_funcs, self.print_func_calls
        for name, func in zip(names, funcs):
            print()
            notify('*', 30, name.capitalize())
            func()

    def print_funcs(self):
        for func_decl in self._func_decls:
            print(func_decl)

    def print_func_calls(self):
        for fcall in self._func_calls:
            print(fcall.repr_as_tree())
            print()
