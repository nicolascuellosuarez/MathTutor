from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):
    """
    Class TokenType created to declare
    the different types of tokens that exist
    in the calculator.
    """

    NUMBER = auto()
    VARIABLE = auto()
    FUNCTION = auto()
    OPERATOR = auto()
    LPAREN = auto()
    RPAREN = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    LBRACE = auto()
    RBRACE = auto()
    EOF = auto()


@dataclass(frozen=True)
class Token:
    """
    Class Token created to reference
    every token in an expression.
    """

    type: TokenType
    value: str
