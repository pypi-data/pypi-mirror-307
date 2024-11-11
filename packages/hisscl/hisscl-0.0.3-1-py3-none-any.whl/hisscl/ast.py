import dataclasses
import typing

@dataclasses.dataclass
class Position:
    name: str = "<unknown>"
    line: int = 1
    col: int = 0
    
    def __str__(self) -> str:
        return f'{self.name}:{self.line}:{self.col}'

@dataclasses.dataclass
class Integer:
    pos: Position
    value: int

@dataclasses.dataclass
class Float:
    pos: Position
    value: float

@dataclasses.dataclass
class Bool:
    pos: Position
    value: bool
    
@dataclasses.dataclass
class String:
    pos: Position
    value: str
    
Literal = Integer | Float | Bool | String
    
@dataclasses.dataclass
class VariableRef:
    pos: Position
    name: str
    
@dataclasses.dataclass
class FunctionCall:
    pos: Position
    name: str
    args: list['Value']

Ref = VariableRef | FunctionCall
    
@dataclasses.dataclass
class Tuple:
    pos: Position
    items: list['Value']

@dataclasses.dataclass
class Object:
    pos: Position
    items: list[tuple['Value', 'Value']]

Collection = Tuple | Object
    
@dataclasses.dataclass
class Operator:
    pos: Position
    value: str
    
@dataclasses.dataclass
class BinaryExpression:
    pos: Position
    left: 'Value'
    op: Operator
    right: 'Value'

@dataclasses.dataclass
class UnaryExpression:
    pos: Position
    op: Operator
    value: 'Value'
    
@dataclasses.dataclass
class Expansion:
    pos: Position
    value: 'Value'
    
Expression = BinaryExpression | UnaryExpression | Expansion
Value = Literal | Collection | Expression | Ref

@dataclasses.dataclass
class Assignment:
    pos: Position
    name: str
    value: Value
    
@dataclasses.dataclass
class Block:
    pos: Position
    name: str
    labels: list[str]
    children: list[Assignment | typing.Self]
    
AST = list[Assignment | Block]