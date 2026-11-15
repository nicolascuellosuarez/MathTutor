import cmath
import math
import operator
from typing import ClassVar, Never
from abc import ABC, abstractmethod

import numpy as np

from .exceptions import (
    IncompleteExpressionError,
    InvalidOperationError,
    UnboundVariableError,
)


class Node(ABC):
    """
    Class Node created to represent an element for
    the calculation tree. It is an abstract class that defines
    the interface for all nodes in the tree.
    """

    @property
    @abstractmethod
    def is_complete(self) -> bool:
        """
        Defines if a node is complete or not.
        """

        raise NotImplementedError

    @property
    @abstractmethod
    def to_latex(self) -> str:
        """
        Returns the LaTeX representation of the node.
        """

        raise NotImplementedError

    @property
    @abstractmethod
    def evaluate(self) -> int | float | complex | bool:
        """
        Returns the evaluation of the node.
        """

        raise NotImplementedError


class NumberNode(Node):
    """
    Class NumberNode created to represent a number
    in the calculation tree. It is a subclass of Node and implements
    the interface defined in the abstract class.
    """

    def __init__(self, value: float | str) -> None:
        self.value: float | str = value

    @property
    def is_complete(self) -> bool:
        """
        Defines if a number node is complete or not.
        """

        return True

    @property
    def to_latex(self) -> str:
        """
        Returns the LaTeX representation of the number node.
        """

        possible_constants = {
            "pi": r"\pi",
            "e": r"e",
            "phi": r"\phi",
            "i": r"i",
        }

        if self.value in possible_constants:
            return str(possible_constants[self.value])
        return str(self.value)

    @property
    def evaluate(self) -> int | float | complex | bool:
        """
        Returns the evaluation of the number node.
        """

        possible_constants = {
            "pi": cmath.pi,
            "e": cmath.e,
            "phi": (1 + cmath.sqrt(5)) / 2,
            "i": cmath.sqrt(-1),
        }

        if self.value in possible_constants:
            return possible_constants[self.value]
        elif isinstance(self.value, str):
            return float(self.value)
        return self.value


class EmptySlot(Node):
    """
    Class EmptySlot created to represent an empty slot
    in the calculation tree. It is a subclass of Node.
    """

    @property
    def is_complete(self) -> bool:
        """
        Defines if an empty slot node is complete or not.
        """

        return False

    @property
    def to_latex(self) -> str:
        """
        Returns the LaTeX representation of the empty slot node.
        """

        return r"\square"

    @property
    def evaluate(self) -> Never:
        """
        Returns an IncompleteExpressionError when
        trying to evaluate an empty node.
        """

        raise IncompleteExpressionError("An empty node has no value.")


class BinaryNode(Node):
    """
    Class BinaryNode created to represent
    binary operations. It is a subclass of
    Node.
    """

    def __init__(self, left: Node | None, right: Node | None, operator: str) -> None:
        if (left is None) and (right is not None):
            self.left: EmptySlot = EmptySlot()
            self.right: Node = right
        elif (right is None) and (left is not None):
            self.left: Node = left
            self.right: EmptySlot = EmptySlot()
        elif (right is None) and (left is None):
            self.left: EmptySlot = EmptySlot()
            self.right: EmptySlot = EmptySlot()
        else:
            self.left: Node = left
            self.right: Node = right

        self.operator: str = operator

    @property
    def is_complete(self) -> bool:
        """
        Defines if a BinaryNode is complete or not.
        """

        return self.left.is_complete and self.right.is_complete

    @property
    def to_latex(self) -> str:
        """
        Returns the LaTeX representation of the BinaryNode.
        """

        LaTeX_symbols = {
            "+": "+",
            "-": "-",
            "*": r"\times",
            "/": r"\div",
            "^": "^",
            "=": "=",
            ">": ">",
            "<": "<",
            ">=": r"\geq",
            "<=": r"\leq",
            "neq": r"\neq",
            "in": r"\in",
            "union": r"\cup",
            "intersect": r"\cap",
            "derivative": r"\frac{d}{dx}",
            "integral": r"\int",
            "sum": r"\sum",
        }

        if self.operator not in LaTeX_symbols:
            raise InvalidOperationError("Operation not supported.")

        
        if self.operator == "^":
            return f"{{{self.left.to_latex}}}^{{{self.right.to_latex}}}"
        elif self.operator == "/":
            return f"\\frac{{{self.left.to_latex}}}{{{self.right.to_latex}}}"

        symbol = LaTeX_symbols[self.operator]
        return f"({self.left.to_latex} {symbol} {self.right.to_latex})"

    @property
    def evaluate(self) -> int | float | complex | bool:
        """
        Evaluates the operation of the BinaryNode.
        """

        math_operations = {
            "+": operator.add,
            "-": operator.sub,
            "*": operator.mul,
            "/": operator.truediv,
            "^": operator.pow,
            "=": operator.eq,
            ">": operator.gt,
            "<": operator.lt,
            ">=": operator.ge,
            "<=": operator.le,
            "neq": operator.ne,
        }

        if self.operator not in math_operations:
            raise InvalidOperationError("Operation not supported.")

        operation_function = math_operations[self.operator]
        return operation_function(self.left.evaluate, self.right.evaluate)


class UnaryNode(Node):
    """
    Class UnaryNode created to represent
    unary operations. It is a subclass of
    Node.
    """

    def __init__(self, operator: str, argument: Node | None) -> None:
        if argument is None:
            self.argument: EmptySlot = EmptySlot()
        else:
            self.argument: Node = argument

        self.operator: str = operator

    @property
    def is_complete(self) -> bool:
        """
        Defines if a UnaryNode is complete or not.
        """

        return self.argument.is_complete

    @property
    def to_latex(self) -> str:
        """
        Returns the LaTeX representation of the UnaryNode.
        """

        LaTeX_symbols = {
            "sqrt": r"\sqrt",
            "cbrt": r"\sqrt[3]",
            "abs": r"\left| \right|",
            "log": r"\log",
            "ln": r"\ln",
            "exp": r"\exp",
            "factorial": r"!",
            "neg": r"-",
            "sin": r"\sin",
            "cos": r"\cos",
            "tan": r"\tan",
            "csc": r"\csc",
            "sec": r"\sec",
            "cot": r"\cot",
            "sinh": r"\sinh",
            "cosh": r"\cosh",
            "tanh": r"\tanh",
            "csch": r"\csch",
            "sech": r"\sech",
            "coth": r"\coth",
            "arcsin": r"\arcsin",
            "arccos": r"\arccos",
            "arctan": r"\arctan",
            "arccsc": r"\arccsc",
            "arcsec": r"\arcsec",
            "arccot": r"\arccot",
            "arsinh": r"\arsinh",
            "arcosh": r"\arcosh",
            "artanh": r"\artanh",
            "arcsch": r"\arcsch",
            "arsech": r"\arsech",
            "arcoth": r"\arcoth",
            "floor": r"\lfloor \rfloor",
            "ceil": r"\lceil \rceil",
        }

        if self.operator not in LaTeX_symbols:
            raise InvalidOperationError("Operation not supported.")

        symbol = LaTeX_symbols[self.operator]

        if self.operator == "sqrt":
            return f"\\sqrt{{{self.argument.to_latex}}}"
        elif self.operator == "cbrt":
            return f"\\sqrt[3]{{{self.argument.to_latex}}}"
        elif self.operator == "abs":
            return f"\\left|{self.argument.to_latex}\\right|"
        elif self.operator == "floor":
            return f"\\lfloor {self.argument.to_latex} \\rfloor"
        elif self.operator == "ceil":
            return f"\\lceil {self.argument.to_latex} \\rceil"
        elif self.operator == "factorial":
            return f"{self.argument.to_latex}!"
        elif self.operator == "neg":
            return f"-{self.argument.to_latex}"

        return f"{symbol}({self.argument.to_latex})"

    @property
    def evaluate(self) -> int | float | complex | bool:
        """
        Evaluates the operation of the UnaryNode.
        """

        math_operator = {
            "sqrt": cmath.sqrt,
            "cbrt": np.cbrt,
            "abs": abs,
            "log": cmath.log10,
            "ln": cmath.log,
            "exp": cmath.exp,
            "factorial": math.factorial,
            "neg": operator.neg,
            "sin": cmath.sin,
            "cos": cmath.cos,
            "tan": cmath.tan,
            "csc": lambda x: 1 / cmath.sin(x),
            "sec": lambda x: 1 / cmath.cos(x),
            "cot": lambda x: 1 / cmath.tan(x),
            "sinh": cmath.sinh,
            "cosh": cmath.cosh,
            "tanh": cmath.tanh,
            "csch": lambda x: 1 / cmath.sinh(x),
            "sech": lambda x: 1 / cmath.cosh(x),
            "coth": lambda x: 1 / cmath.tanh(x),
            "arcsin": cmath.asin,
            "arccos": cmath.acos,
            "arctan": cmath.atan,
            "arccsc": lambda x: cmath.asin(1 / x),
            "arcsec": lambda x: cmath.acos(1 / x),
            "arccot": lambda x: cmath.atan(1 / x),
            "arsinh": cmath.asinh,
            "arcosh": cmath.acosh,
            "artanh": cmath.atanh,
            "arcsch": lambda x: cmath.asinh(1 / x),
            "arsech": lambda x: cmath.acosh(1 / x),
            "arcoth": lambda x: cmath.atanh(1 / x),
            "floor": math.floor,
            "ceil": math.ceil,
        }

        if self.operator not in math_operator:
            raise InvalidOperationError("Operation not supported.")

        operation_function = math_operator[self.operator]
        return operation_function(self.argument.evaluate)


class VariableNode(Node):
    """
    Class VariableNode created to represent a
    variable in the calculator. It is a
    subclass of Node.
    """

    dictionary_of_greek_letters: ClassVar = {
        "alpha": r"\alpha",
        "Alpha": r"A",
        "beta": r"\beta",
        "Beta": r"B",
        "gamma": r"\gamma",
        "Gamma": r"\Gamma",
        "delta": r"\delta",
        "Delta": r"\Delta",
        "epsilon": r"\epsilon",
        "Epsilon": r"E",
        "zeta": r"\zeta",
        "Zeta": r"Z",
        "eta": r"\eta",
        "Eta": r"H",
        "theta": r"\theta",
        "Theta": r"\Theta",
        "iota": r"\iota",
        "Iota": r"I",
        "kappa": r"\kappa",
        "Kappa": r"K",
        "lambda": r"\lambda",
        "Lambda": r"\Lambda",
        "mu": r"\mu",
        "Mu": r"M",
        "nu": r"\nu",
        "Nu": r"N",
        "xi": r"\xi",
        "Xi": r"\Xi",
        "omicron": r"o",
        "Omicron": r"O",
        "pi": r"\pi",
        "Pi": r"\Pi",
        "rho": r"\rho",
        "Rho": r"P",
        "sigma": r"\sigma",
        "Sigma": r"\Sigma",
        "tau": r"\tau",
        "Tau": r"T",
        "upsilon": r"\upsilon",
        "Upsilon": r"Y",
        "phi": r"\phi",
        "Phi": r"\Phi",
        "chi": r"\chi",
        "Chi": r"X",
        "psi": r"\psi",
        "Psi": r"\Psi",
        "omega": r"\omega",
        "Omega": r"\Omega",
    }

    def __init__(self, name: str) -> None:
        self.name: str = name

    @property
    def is_complete(self) -> bool:
        """
        Defines if a VariableNode is complete
        or not.
        """

        return bool(self.name)

    @property
    def to_latex(self) -> str:
        """
        Returns the LaTeX representation of a
        VariableNode.
        """

        if self.name in VariableNode.dictionary_of_greek_letters:
            return VariableNode.dictionary_of_greek_letters[self.name]
        return f"{self.name}"

    @property
    def evaluate(self) -> Never:
        """
        Returns the evaluation of a VariableNode,
        not implemented.
        """

        raise UnboundVariableError(f"La variable {self.name} no tiene valor.")
