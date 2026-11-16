from typing import ClassVar

from .exceptions import InvalidNumberError
from .tokens import Token, TokenType


class Lexer:
    """
    Transforms mathematical expressions into Token objects.
    """

    OPERATORS: ClassVar = {
        "+",
        "-",
        "*",
        "/",
        "^",
        "=",
        ">",
        "<",
        ">=",
        "<=",
        "neq",
    }

    DELIMITERS: ClassVar = {
        "(": TokenType.LPAREN,
        ")": TokenType.RPAREN,
        "[": TokenType.LBRACKET,
        "]": TokenType.RBRACKET,
        "{": TokenType.LBRACE,
        "}": TokenType.RBRACE,
    }

    FUNCTIONS: ClassVar = {
        "sqrt",
        "cbrt",
        "abs",
        "log",
        "ln",
        "exp",
        "factorial",
        "neg",
        "sin",
        "cos",
        "tan",
        "csc",
        "sec",
        "cot",
        "sinh",
        "cosh",
        "tanh",
        "csch",
        "sech",
        "coth",
        "arcsin",
        "arccos",
        "arctan",
        "arccsc",
        "arcsec",
        "arccot",
        "arsinh",
        "arcosh",
        "artanh",
        "arcsch",
        "arsech",
        "arcoth",
        "floor",
        "ceil",
    }

    CONSTANTS: ClassVar = {"pi", "e", "phi", "i"}

    GREEK_LETTERS: ClassVar = {
        "alpha",
        "Alpha",
        "beta",
        "Beta",
        "gamma",
        "Gamma",
        "delta",
        "Delta",
        "epsilon",
        "Epsilon",
        "zeta",
        "Zeta",
        "eta",
        "Eta",
        "theta",
        "Theta",
        "iota",
        "Iota",
        "kappa",
        "Kappa",
        "lambda",
        "Lambda",
        "mu",
        "Mu",
        "nu",
        "Nu",
        "xi",
        "Xi",
        "omicron",
        "Omicron",
        "pi",
        "Pi",
        "rho",
        "Rho",
        "sigma",
        "Sigma",
        "tau",
        "Tau",
        "upsilon",
        "Upsilon",
        "phi",
        "Phi",
        "chi",
        "Chi",
        "psi",
        "Psi",
        "omega",
        "Omega",
    }

    def __init__(self, expression: str) -> None:
        self.expression: str = expression
        self.position: int = 0

    def tokenize(self) -> list[Token]:
        """
        Transforms the expression into a list of tokens.
        """

        list_of_tokens: list[Token] = []

        while self.position < len(self.expression):
            character = self.expression[self.position]

            if character.isspace():
                self.position += 1

            elif character.isdigit():
                list_of_tokens.append(self._read_number())

            elif character.isalpha() or character == "_":
                list_of_tokens.append(self._read_identifier())

            elif character in self.DELIMITERS:
                list_of_tokens.append(Token(self.DELIMITERS[character], character))
                self.position += 1

            elif character in {">", "<", "="}:
                if (
                    self.position + 1 < len(self.expression)
                    and self.expression[self.position + 1] == "="
                    and character in {">", "<"}
                ):
                    list_of_tokens.append(Token(TokenType.OPERATOR, character + "="))
                    self.position += 2
                else:
                    list_of_tokens.append(Token(TokenType.OPERATOR, character))
                    self.position += 1

            elif character in self.OPERATORS:
                list_of_tokens.append(Token(TokenType.OPERATOR, character))
                self.position += 1

            else:
                raise ValueError(
                    f"Unknown character '{character}' at position {self.position}."
                )

        list_of_tokens.append(Token(TokenType.EOF, ""))

        return list_of_tokens

    def _read_number(self) -> Token:
        """
        Reads an entire number, including decimals.
        """

        has_a_decimal = False
        starting_position = self.position

        if (
            self.position >= len(self.expression)
            or not self.expression[self.position].isdigit()
        ):
            raise InvalidNumberError("Number is not valid.")

        while self.position < len(self.expression):
            character = self.expression[self.position]

            if character.isdigit():
                self.position += 1

            elif character == ".":
                if has_a_decimal:
                    raise InvalidNumberError("Number is not valid.")

                if (
                    self.position + 1 >= len(self.expression)
                    or not self.expression[self.position + 1].isdigit()
                ):
                    raise InvalidNumberError("Number is not valid.")

                has_a_decimal = True
                self.position += 1

            else:
                break

        return Token(
            TokenType.NUMBER, self.expression[starting_position : self.position]
        )

    def _read_identifier(self) -> Token:
        """
        Reads functions, constants, Greek letters and variables.
        """

        starting_position = self.position

        while self.position < len(self.expression):
            character = self.expression[self.position]

            if character.isalnum() or character == "_":
                self.position += 1
            else:
                break

        identifier = self.expression[starting_position : self.position]

        if identifier in self.FUNCTIONS:
            token_type = TokenType.FUNCTION

        elif identifier == "neq":
            token_type = TokenType.OPERATOR

        elif identifier in self.CONSTANTS:
            token_type = TokenType.CONSTANT

        elif identifier in self.GREEK_LETTERS:
            token_type = TokenType.VARIABLE

        else:
            token_type = TokenType.VARIABLE

        return Token(token_type, identifier)
