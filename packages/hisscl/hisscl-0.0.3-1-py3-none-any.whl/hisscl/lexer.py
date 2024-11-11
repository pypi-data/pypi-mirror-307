from . import ast

import io
import enum
import typing
import dataclasses

__all__ = ['Token', 'ExpectedError', 'Lexer', 'is_whitespace', 'is_operator', 'is_numeric', 'is_alpha', 'is_alphanum']

class Token(enum.Enum):
    ILLEGAL = -1
    EOF = 0

    COMMENT = 1
    IDENT = 2
    STRING = 3
    BOOL = 4
    INTEGER = 5
    FLOAT = 6
    HEREDOC = 7
    CURLY = 8
    SQUARE = 9
    PAREN = 10
    COMMA = 11
    COLON = 12
    OPERATOR = 13
    ELLIPSIS = 14

class ExpectedError(Exception):
    def __init__(self, pos: ast.Position, expected: str, got: str):
        super().__init__(f'{pos}: expected {expected}, got {"EOF" if got == '' else repr(got)}')
        self.pos = pos
        self.got = got
        self.expected = expected

class Lexer:
    pos = ast.Position()
    prev_pos = ast.Position()
    unread = ''

    def __init__(self, stream: typing.TextIO, name: str):
        self.stream = stream
        self.pos.name = name

    def _peek(self, n: int) -> str:
        if self.unread != '':
            return self.unread
        pos = self.stream.tell()
        text = self.stream.read(n)
        self.stream.seek(pos)
        return text

    def _read(self) -> str:
        char = self.unread
        if self.unread != '':
            self.unread = ''

        if char == '':
            char = self.stream.read(1)

        self.prev_pos = dataclasses.replace(self.pos)
        if char == '\n':
            self.pos.line += 1
            self.pos.col = 1
        elif char != '':
            self.pos.col += 1
        return char

    def _unread(self, char):
        self.pos = self.prev_pos
        self.unread = char

    def _scan_str(self) -> tuple[Token, ast.Position, str]:
        pos = dataclasses.replace(self.pos)
        with io.StringIO() as out:
            out.write('"')
            escape = False
            char = self._read()
            while True:
                if char == '"' and escape:
                    escape = False
                    out.write('\\"')
                elif char == '\\' and escape:
                    escape = False
                    out.write('\\\\')
                elif char == '\\':
                    escape = True
                elif char == '"':
                    break
                elif char == '' or char == '\r' or char == '\n':
                    raise ExpectedError(self.pos, repr('"'), char)
                elif escape:
                    escape = False
                    out.write('\\' + char)
                else:
                    out.write(char)

                char = self._read()
            out.write('"')
            return Token.STRING, pos, out.getvalue()

    def _scan_number(self, char: str) -> tuple[Token, ast.Position, str]:
        pos = dataclasses.replace(self.pos)
        tok = Token.INTEGER
        with io.StringIO() as out:
            while True:
                if is_numeric(char):
                    out.write(char)
                elif char == '.':
                    if tok == Token.FLOAT:
                        raise ExpectedError(self.pos, "number", char)
                    tok = Token.FLOAT
                    out.write(char)
                else:
                    self._unread(char)
                    return tok, pos, out.getvalue()
                char = self._read()

    def _scan_ident(self, char: str) -> tuple[Token, ast.Position, str]:
        pos = dataclasses.replace(self.pos)
        with io.StringIO() as out:
            while is_alphanum(char) or char in ('-', '_'):
                out.write(char)
                char = self._read()
            self._unread(char)
            val = out.getvalue()
            if val in ('true', 'false'):
                return Token.BOOL, pos, val
            else:
                return Token.IDENT, pos, out.getvalue()

    def _scan_comment(self, char: str) -> tuple[Token, ast.Position, str]:
        pos = dataclasses.replace(self.pos)
        with io.StringIO() as out:
            while char != '\n' and char != '':
                if char != '\r':
                    out.write(char)
                char = self._read()
            return Token.COMMENT, pos, out.getvalue()
    
    def _scan_inline_comment(self, char: str) -> tuple[Token, ast.Position, str]:
        pos = dataclasses.replace(self.pos)
        with io.StringIO() as out:
            while True:
                if char == '*' and self._peek(1) == '/':
                    self._read()
                    break
                out.write(char)
                char = self._read()
            return Token.COMMENT, pos, out.getvalue()

    def _scan_heredoc(self, char: str) -> tuple[Token, ast.Position, str]:
        pos = dataclasses.replace(self.pos)
        with io.StringIO() as out:
            char = self._read()
            if char != '<':
                raise ExpectedError(self.pos, repr('<'), char)

            char = self._read()
            if not is_alpha(char):
                raise ExpectedError(self.pos, 'heredoc name', char)

            _, _, heredoc_name = self._scan_ident(char)
            name_len = len(heredoc_name) - 1

            char = self._read()
            while True:
                if char == heredoc_name[0] and self._peek(name_len) == heredoc_name[1:]:
                    self.pos.col += name_len
                    self.stream.seek(self.stream.tell()+name_len)
                    break
                else:
                    out.write(char)
                char = self._read()

            return Token.HEREDOC, pos, out.getvalue()
            
    # TODO: scan multi-char operators like ==
    def _scan_operator(self, char) -> tuple[Token, ast.Position, str]:
        pos = dataclasses.replace(self.pos)
        with io.StringIO() as out:
            while is_operator(char):
                out.write(char)
                char = self._read()
            self._unread(char)
            val = out.getvalue()
            return Token.OPERATOR, pos, out.getvalue()

    def scan(self) -> tuple[Token, ast.Position, str]:
        char = self._read()
        while is_whitespace(char):
            char = self._read()

        match char:
            case '{' | '}':
                return Token.CURLY, self.pos, char
            case '[' | ']':
                return Token.SQUARE, self.pos,  char
            case '(' | ')':
                return Token.PAREN, self.pos, char
            case ',':
                return Token.COMMA, self.pos, char
            case ':':
                return Token.COLON, self.pos, char
            case '"':
                    return self._scan_str()
            case '<':
                # If the next character is not another less than symbol,
                # this is probably a less than operator.
                if self._peek(1) != '<':
                    return Token.OPERATOR, self.pos, char
                return self._scan_heredoc(char)
            case '/':
                    next = self._peek(1)
                    if next == '/':
                        # Ignore comment and return next token
                        self._scan_comment(char)
                        return self.scan()
                    elif next == '*':
                        # Ignore inlinecomment and return next token
                        self._scan_inline_comment(char)
                        return self.scan()
                    else:
                        # If the next character is not another slash
                        # or an asterisk, this is probably a division
                        # operator.
                        return Token.OPERATOR, self.pos, char
            case '#':
                # Ignore comments and return next token
                self._scan_comment(char)
                return self.scan()
            case '.':
                if (next := self._read()) != '.':
                    raise ExpectedError(self.pos, '.', next)
                if (next := self._read()) != '.':
                    raise ExpectedError(self.pos, '.', next)
                return Token.ELLIPSIS, self.pos, "..."
            case '':
                return Token.EOF, self.pos, char

        if is_numeric(char):
            return self._scan_number(char)
        elif is_alpha(char):
            return self._scan_ident(char)
        elif is_operator(char):
            return self._scan_operator(char)

        return Token.ILLEGAL, self.pos, char

def is_whitespace(char: str) -> bool:
    return char in (' ', '\t', '\r', '\n')

def is_operator(char: str) -> bool:
    return char in ('=', '+', '-', '*', '/', '%', '!', '>', '<', '|', '&')

def is_numeric(char: str) -> bool:
    return char >= '0' and char <= '9'

def is_alpha(char: str) -> bool:
    return (char >= 'a' and char <= 'z') or (char >= 'A' and char <= 'Z')

def is_alphanum(char: str) -> bool:
    return is_numeric(char) or is_alpha(char)
