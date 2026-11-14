from .exceptions import IncompleteExpressionError, InvalidOperationError
import operator
import math
import cmath
import numpy as np


class Node():
    """
    Class Node created to represent an element for
    the calculation tree. It is an abstract class that defines 
    the interface for all nodes in the tree.
    """

    @property
    def is_complete(self) -> bool:
        """
        Defines if a node is complete or not.
        """
        
        raise NotImplementedError

    @property
    def to_latex(self) -> str:
        """
        Returns the LaTeX representation of the node.
        """

        raise NotImplementedError

    @property
    def evaluate(self) -> str:
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
    
    def __init__(self, value: int) -> None:
        self.value: float = value

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

        return str(self.value)

    @property
    def evaluate(self) -> str:
        """
        Returns the evaluation of the number node.
        """

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
    def evaluate(self) -> float:
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
        elif (right is None) and (left is not None):
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

        if (self.left.is_complete == True) and (self.right.is_complete == True):
            return True
        return False

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
            "sum": r"\sum"
        }
        
        if self.operator not in LaTeX_symbols:
            raise InvalidOperationError("Operation not supported.")

        symbol = LaTeX_symbols[self.operator]
        return f"{self.left.to_latex} {symbol} {self.right.to_latex}"

    @property
    def evaluate(self) -> float:
        """
        Evaluates the operation of the BinaryNode.
        """

        math_operations = {
            "+": operator.add,
            "-": operator.sub,
            "*": operator.mul,
            "/": operator.truediv,
            "^": operator.pow,
            "sqrt": lambda left, right: left ** 0.5,
            "=": operator.eq,
            ">": operator.gt,
            "<": operator.lt,
            ">=": operator.ge,
            "<=": operator.le,
            "neq": operator.ne
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
            "cbrt": r"\cbrt",
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
            "ceil": r"\lceil \rceil"
        }

        if self.operator not in LaTeX_symbols:
            raise InvalidOperationError("Operation not supported.")

        symbol = LaTeX_symbols[self.operator]
        return f"{symbol}({self.argument.to_latex})"

    @property
    def evaluate(self):
        """
        Evaluates the operation of the UnaryNode.
        """

        math_operator = {
            "sqrt": cmath.sqrt,
            "cbrt": np.cbrt,
            "abs": abs,
            "log": cmath.log,
            "ln": cmath.ln,
            "exp": cmath.exp,
            "factorial": math.factorial,
            "neg": operator.neg,
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
            "ceil": r"\lceil \rceil"
        }
    