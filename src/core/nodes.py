from .exceptions import IncompleteExpressionError, InvalidOperationError


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
        
        raise InvalidOperationError

    @property
    def to_latex(self) -> str:
        """
        Returns the LaTeX representation of the node.
        """

        raise InvalidOperationError

    @property
    def evaluate(self) -> str:
        """
        Returns the evaluation of the node.
        """

        raise InvalidOperationError


class NumberNode(Node):
    """
    Class NumberNode created to represent a number
    in the calculation tree. It is a subclass of Node and implements
    the interface defined in the abstract class.
    """
    
    def __init__(self, value: int) -> None:
        self.value: int = value

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
    
