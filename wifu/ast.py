from typing import Any


class FuncArg:
    pass


class FuncBody:
    pass


class FuncCall:
    def __init__(self, name: str):
        self._name = name
        self._args = []

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


class Func:
    def __init__(self, name: str, start: int, args: list[FuncArg], body: FuncBody):
        self._name = name
        self._start = start
        self._args = args
        self._body = body

    def __str__(self):
        return f'Func[{self._name}, start {self._start}, args {len(self._args)}]'

    def __repr__(self):
        return self.__str__()


class IndentationProblem(Exception):
    pass


def is_func_call(line: str) -> bool:
    if len(line) == 0 or line.startswith(' ') or line.startswith('\t'):
        return False
    if 'func' not in line:
        return True
    s = line[line.index('func')+len('func'):]
    spaces = s.count(' ')
    tabs = s.count('\t')
    return len(s) and (len(s) - spaces - tabs > 0)


def is_func(line: str) -> bool:
    return line.strip() == 'func'


def define_line_indent(line: str) -> int:
    if not len(line):
        return 0
    i = 0
    while line[i] in (' ', '\t'):
        i += 1
    return i


def skip_empty_lines(code: str, line_num: int) -> int:
    while not code[line_num].strip():
        line_num += 1
    return line_num


def get_func_name(code: str, line_num: int, base_indent: int) -> (str, int):
    line_num += 1
    line_num = skip_empty_lines(code, line_num)
    func_name = code[line_num].strip()
    if base_indent >= define_line_indent(code[line_num]):
        raise IndentationProblem('problem with indentation of function name')
    return func_name, line_num


def get_func_args(code: str, line_num: int, base_indent: int) -> (list[FuncArg], int):
    line_num += 1
    line_num = skip_empty_lines(code, line_num)
    if code[line_num].strip() != 'args':
        line_num -= 1
        return [],line_num
    # UNIMPLEMENTED(kra53n)
    return [], line_num


def get_func_body(code: str, line_num: int, base_indent: int) -> (FuncBody, int):
    # UNIMPLEMENTED(kra53n)
    line_num += 1
    line_num = skip_empty_lines(code, line_num)
    body: list[Statement] = []
    while (line_num < len(code) and
           (indent := define_line_indent(code[line_num])) and
           indent > base_indent):
        body.append(code[line_num])
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
                raise IndentationProblem()

        if line_indent == indent:
            func_call.add(code[line_num].strip())
        elif line_indent > indent:
            func_call.pop()
            inner_func_call, line_num = parse_func_call(code, line_num-1)
            func_call.add(inner_func_call)
        else:
            break
    return func_call, line_num


def parse_func(code: list[str], line_num: int) -> (Func, int):
    start = line_num
    indent = define_line_indent(code[line_num])
    func_name, line_num = get_func_name(code, line_num, indent)
    args, line_num = get_func_args(code, line_num, indent)
    body, line_num = get_func_body(code, line_num, indent)
    return Func(func_name, start, args, body), line_num


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
        self._func_calls: list[FuncCall] = []
        self._funcs: list[Func] = []
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
            elif is_func(line):
                func, line_num = parse_func(code, line_num)
                self._funcs.append(func)
            line_num += 1

    def print(self):
        print(self._func_calls)
        print(self._funcs)
