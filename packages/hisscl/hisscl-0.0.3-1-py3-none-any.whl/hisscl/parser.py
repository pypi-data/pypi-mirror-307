from . import ast
from . import lexer

from typing import TextIO

import ast as pyast

__all__ = ['ExpectedError', 'Parser']

class ExpectedError(Exception):
    def __init__(self, pos: ast.Position, expected: str, got: str):
        super().__init__(f'{pos}: expected {expected}; got {"EOF" if got == '' else repr(got)}')
        self.pos = pos
        self.got = got
        self.expected = expected

class Parser:
    _prev: tuple[lexer.Token, ast.Position, str] | None = None
    
    def __init__(self, stream: TextIO, name: str):
        self.lexer = lexer.Lexer(stream, name)
        
    def _scan(self) -> tuple[lexer.Token, ast.Position, str]:
        if self._prev is not None:
            prev = self._prev
            self._prev = None
            return prev
        return self.lexer.scan()
    
    def _unscan(self, tok: lexer.Token, pos: ast.Position, lit: str):
        self._prev = tok, pos, lit
        
    def _parse_expr(self) -> ast.Value:
        left = self._parse_value()
        tok, pos, lit = self._scan()
        if tok != lexer.Token.OPERATOR:
            self._unscan(tok, pos, lit)
            return left
        right = self._parse_expr()
        return ast.BinaryExpression(pos=left.pos, op=ast.Operator(pos=pos, value=lit), left=left, right=right)
        
    def _parse_tuple(self, start_pos: ast.Position) -> ast.Tuple:
        items: list[ast.Value] = []
        while True:
            tok, pos, lit = self._scan()
            if tok == lexer.Token.SQUARE and lit == ']':
                break
            self._unscan(tok, pos, lit)
            items.append(self._parse_expr())
            
            tok, pos, lit = self._scan()
            if tok != lexer.Token.COMMA and (tok != lexer.Token.SQUARE or lit != ']'):
                raise ExpectedError(pos, 'comma or closing square bracket', lit)
            elif tok == lexer.Token.SQUARE and lit == ']':
                break
        return ast.Tuple(start_pos, items)
        
    def _parse_object(self, start_pos: ast.Position) -> ast.Object:
        items: list[tuple[ast.Value, ast.Value]] = []
        while True:
            tok, pos, lit = self._scan()
            if tok == lexer.Token.CURLY and lit == '}':
                break
            self._unscan(tok, pos, lit)
            key = self._parse_expr()
            
            tok, pos, lit = self._scan()
            if tok != lexer.Token.COLON and (tok != lexer.Token.OPERATOR or lit != '='):
                raise ExpectedError(pos, 'colon or equals sign', lit)
                
            val = self._parse_expr()
            items.append((key, val))
            
            tok, pos, lit = self._scan()
            if tok != lexer.Token.COMMA:
                self._unscan(tok, pos, lit)
            
        return ast.Object(start_pos, items)
        
    def _parse_func_call(self) -> ast.FunctionCall:
        id_tok, id_pos, id_lit = self._scan()
        tok, pos, lit = self._scan()
        if tok != lexer.Token.PAREN or lit != '(':
            raise ExpectedError(pos, 'opening parentheses', lit)
        
        tok, pos, lit = self._scan()
        if tok == lexer.Token.PAREN and lit == ')':
            return ast.FunctionCall(pos=id_pos, name=id_lit, args=[])
        self._unscan(tok, pos, lit)
        
        args: list[ast.Value] = []
        while True:
            args.append(self._parse_expr())
            tok, pos, lit = self._scan()
            if tok == lexer.Token.PAREN and lit == ')':
                break
            elif tok == lexer.Token.COMMA:
                continue
            elif tok == lexer.Token.ELLIPSIS:
                args[-1] = ast.Expansion(pos=args[-1].pos, value=args[-1])
                tok, pos, lit = self._scan()
                if tok != lexer.Token.PAREN or lit != ')':
                    raise ExpectedError(pos, 'closing parentheses', lit)
                break
            else:
                raise ExpectedError(pos, 'comma or closing parentheses', lit)
        return ast.FunctionCall(pos=id_pos, name=id_lit, args=args)
    
    def _parse_value(self) -> ast.Value:
        tok, pos, lit = self._scan()
        match tok:
            case lexer.Token.INTEGER:
                return ast.Integer(pos=pos, value=int(lit))
            case lexer.Token.FLOAT:
                return ast.Float(pos=pos, value=float(lit))
            case lexer.Token.BOOL:
                return ast.Bool(pos=pos, value=(lit == 'true'))
            case lexer.Token.STRING:
                return ast.String(pos=pos, value=pyast.literal_eval(lit))
            case lexer.Token.IDENT:
                if self.lexer._peek(1) == '(':
                    self._unscan(tok, pos, lit)
                    return self._parse_func_call()
                return ast.VariableRef(pos=pos, name=lit)
            case lexer.Token.HEREDOC:
                return ast.String(pos=pos, value=lit)
            case lexer.Token.OPERATOR:
                return ast.UnaryExpression(pos=pos, op=ast.Operator(pos=pos, value=lit), value=self._parse_value())
            case lexer.Token.SQUARE:
                if lit != '[':
                    raise ExpectedError(pos, repr('['), lit)
                return self._parse_tuple(pos)
            case lexer.Token.CURLY:
                if lit != '{':
                    raise ExpectedError(pos, repr('{'), lit)
                return self._parse_object(pos)
            case lexer.Token.PAREN:
                if lit != '(':
                    raise ExpectedError(pos, repr('('), lit)
                expr = self._parse_expr()
                tok, pos, lit = self._scan()
                if tok != lexer.Token.PAREN or lit != ')':
                    raise ExpectedError(pos, repr(')'), lit)
                return expr
            
        raise ExpectedError(pos, 'value', lit)
        
    def parse(self, until: tuple[lexer.Token, str] = (lexer.Token.EOF, '')) -> ast.AST:
        tree = []
        while True:
            id_tok, id_pos, id_lit = self._scan()
            if id_tok == until[0] and id_lit == until[1]:
                break
            
            if id_tok != lexer.Token.IDENT:
                raise ExpectedError(id_pos, str(lexer.Token.IDENT), id_lit)
            
            tok, pos, lit = self._scan()
            if tok == lexer.Token.OPERATOR and lit == '=':
                tree.append(ast.Assignment(pos=id_pos, name=id_lit, value=self._parse_expr()))
            elif tok == lexer.Token.CURLY and lit == '{':
                tree.append(ast.Block(pos=id_pos, name=id_lit, labels=[], children=self.parse(until=(lexer.Token.CURLY, '}'))))
            elif tok in (lexer.Token.STRING, lexer.Token.IDENT):
                labels = []
                while tok in (lexer.Token.STRING, lexer.Token.IDENT):
                    if tok == lexer.Token.IDENT:
                        labels.append(lit)
                    else:
                        self._unscan(tok, pos, lit)
                        val = self._parse_value()
                        assert isinstance(val, ast.String)
                        labels.append(val.value)
                    tok, pos, lit = self._scan()
                if tok != lexer.Token.CURLY and lit != '{':
                    raise ExpectedError(pos, repr('{'), lit)
                tree.append(ast.Block(pos=id_pos, name=id_lit, labels=labels, children=self.parse(until=(lexer.Token.CURLY, '}'))))
            else:
                raise ExpectedError(pos, "equals sign, opening curly brace, or string", lit)
        return tree