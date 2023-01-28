from . import err
import re, ast

import copy

EOF = '\0'

exp = re.compile

SYMS = r"_a-zA-Zα-ωΑ-Ω\+\-\=\<\>\*\/\%\^\&\:\$\£\#\~\`\|\\\¬\,\.\?\!\@"
IDENT_STR = r"[{syms}][0-9\'{syms}]*".format(syms=SYMS)
                                         # e.g.
L_PAREN    = exp(r"\A\(")                # '('
R_PAREN    = exp(r"\A\)")                # ')'
NIL        = exp(r"\Anil")               # 'nil'
SYMBOL     = exp(r"\A" + IDENT_STR)      # 'hello-world'
UNEVAL     = exp(r"\A\'")                # '
ATOM       = exp(r"\A\:+[0-9" + IDENT_STR[1:])  # ':good-bye'
NUMERIC    = exp(r"\A[0-9]+(\.[0-9]+)?([xob][0-9a-fA-F]+)?(e[\+\-]?)?[0-9a-fA-F]*")
TERMINATOR = exp(r"\A\n")
STRING     = exp(r"\A([\"'])((\\{2})*|(.*?[^\\](\\{2})*))\1")

impl_loc = {'line':-1,'column':-1, 'filename':'IMPLICIT'}
class Token(object):
    def __init__(self, token_type, string, loc=impl_loc):
        self.type = token_type
        self.string = string
        self.location = loc
        self.location['span'] = len(string) + [0, 2][self.type == 'STRING']

    def __str__(self):
        return "<Token({}) '{}' ({}:{}) [span: {}]>".format(
            self.type,
            self.string,
            self.location['line'],
            self.location['column'],
            self.location['span']
        )

EOF_TOKEN = Token('EOF', EOF)

class TokenStream(object):
    def __init__(self, file, tokens = None):
        self.file = file
        self.tokens = tokens or []
        self.i = 0

    def current(self):
        if self.i >= self.size():
            return EOF_TOKEN
        return self.tokens[self.i]

    def size(self):
        return len(self.tokens)

    def push(self, token):
        if type(token) is list:
            for elem in token:
                self.tokens.append(elem)
        else:
            self.tokens.append(token)
        return self.tokens
    add = push

    def pop(self, j = -1):
        return self.tokens.pop(j)

    def next(self, j = 1):
        self.i += j
        if self.i >= self.size():
            return EOF_TOKEN
        return self.tokens[self.i]

    def ahead(self, j = 1):
        if self.i + j >= self.size():
            return EOF_TOKEN
        return self.tokens[self.i + j]

    def back(self, j = 1):
        self.i -= j
        return self.tokens[self.i]

    def behind(self, j = 1):
        return self.tokens[self.i - j]

    def purge(self, type):
        new = []
        for e in self.tokens:
            if e.type != type:
                new.append(e)
        self.tokens = new
        return new

    def __str__(self):
        def form(s): 
            loc = [s.location['line'], s.location['column']]
            return '<Token({}) {} {} ... {}>'.format(
                s.type,
                '.' * (24 - (len(s.type) + len(str(loc)))),
                loc,
                repr(s.string)
            )
        return '\n'.join(map(form, self.tokens))

def paren_balancer(stream):
    stream = copy.copy(stream)  
    stack = []                  
    balanced = True
    location = None

    while stream.current() != EOF_TOKEN:
        location = stream.current().location
        if stream.current().type == 'L_PAREN':
            stack.append(0)
        elif stream.current().type == 'R_PAREN':
            if len(stack) == 0:
                balanced = False
                break
            else:
                stack.pop()

        stream.next()

    opens = 0
    close = 0
    for t in stream.tokens: 
        if t.type == 'L_PAREN': opens += 1
        if t.type == 'R_PAREN': close += 1

    message = ('Unbalanced amount of parentheses,\n'
        + 'consider removing {} of them...'.format(close - opens))
    if len(stack) != 0:
        location = stream.tokens[-2].location
        message = 'Missing {} closing parentheses...'.format(len(stack))
    elif close - opens < 1:
        message = 'Invalid arrangement of parentheses, this means nothing.'
    return {
        'balanced': balanced and len(stack) == 0,
        'location': location,
        'message': message
    }

def lex(string, file, nofile=False):
    EX = err.Thrower(err.LEX, file)
    filename = file
    if nofile:
        EX.nofile(string)

    string += EOF
    stream = TokenStream(file)
    i = 0
    line = 1  
    column = 1

    match = None 
    while i < len(string):
        partial = string[i::] 

        if partial[0] == EOF:
            stream.add(Token('EOF', partial[0], {
                'line': line,
                'column': column,
                'filename': filename
            }))
            break

        if partial[0] == ';':
            j = 0
            while partial[j] != '\n' and partial[j] != EOF:
                j += 1
            i += j
            column += j
            continue

        if partial[0] == '(':
            stream.add(Token('L_PAREN', partial[0], {
                'line': line,
                'column': column,
                'filename': filename
            }))
            i += 1
            column += 1
            continue

        if partial[0] == ')':
            stream.add(Token('R_PAREN', partial[0], {
                'line': line,
                'column': column,
                'filename': filename
            }))
            i += 1
            column += 1
            continue

        if partial[:3] == 'nil' and not SYMBOL.match(partial[3]):
            stream.add(Token('NIL', partial[:3], {
                'line': line,
                'column': column,
                'filename': filename
            }))
            i += 3
            column += 3
            continue

        if partial[0] == "'":
            stream.add(Token('UNEVAL', "'", {
                'line': line,
                'column': column,
                'filename': filename
            }))
            i += 1
            column += 1
            continue

        if partial[0] == '"':
            contents = ""
            j = 1
            loc = {'line': line, 'column': column, 'filename': filename}
            while partial[j] != '"':
                if partial[j+1] == EOF:
                    l = {'line': line, 'column': column+1, 'filename': filename}
                    EX.throw(l,
                        'Unexpected EOF while reading string,\n'
                        + 'please check that you closed your quote...')
                    stream = TokenStream(stream.file)
                    stream.add(Token('NIL', 'nil', l))
                    return stream
                if partial[j] == '\n':
                    contents += '\\n'
                    line += 1
                    column = 1
                    j += 1
                    continue
                if partial[j] == '\\':
                    contents += '\\' + partial[j+1]
                    j += 2
                    column += 1
                    continue
                contents += partial[j]
                column += 1
                j += 1

            contents = '"' + contents + '"'
            stream.add(Token('STRING', ast.literal_eval(contents), loc))
            i += j + 1
            column += 2
            continue

        match = ATOM.match(partial)
        if match:
            stream.add(Token('ATOM', match.group(), {
                'line': line,
                'column': column,
                'filename': filename
            }))
            span = len(match.group())
            i += span
            column += span
            continue

        match = SYMBOL.match(partial)
        if match:
            stream.add(Token('SYMBOL', match.group(), {
                'line': line,
                'column': column,
                'filename': filename
            }))
            span = len(match.group())
            i += span
            column += span
            continue

        match = NUMERIC.match(partial)
        if match:
            stream.add(Token('NUMERIC', match.group(), {
                'line': line,
                'column': column,
                'filename': filename
            }))
            span = len(match.group())
            i += span
            column += span
            continue

        column += 1 
        if partial[0] == "\n":
            stream.add(Token('TERMINATOR', "\n", {
                'line': line,
                'column': column - 1,
                'filename': filename
            }))
            i += 1
            line += 1
            column = 1
            continue
        i += 1

    balancer = paren_balancer(stream)
    if not balancer['balanced']:
        EX.throw(balancer['location'], balancer['message'])
        stream = TokenStream(stream.file)
        stream.add(Token('NIL', 'nil', balancer['location']))

    return stream
