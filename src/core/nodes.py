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

    def __init__(self, left: Node | None, right: Node | None) -> None:
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

        raise NotImplementedError()

    @property
    def evaluate(self) -> float:
        """
        Raises a NotImplementedError() when
        trying to evaluate a BinaryNode.
        """

        raise NotImplementedError()


class UnaryNode(Node):
    """
    Class UnaryNode created to represent
    unary operations. It is a subclass of
    Node.
    """

    def __init__(self, argument: Node | None) -> None:
        if argument is None:
            self.argument: EmptySlot = EmptySlot()
        else:
            self.argument: Node = argument

    @property
    def is_complete(self) -> bool:
        """
        Defines if a UnaryNode is complete or not.
        """
        
        if self.argument.is_complete:
            return True
        return False

    @property
    def to_latex(self) -> str:
        """
        Returns the LaTeX representation of the UnaryNode.
        """

        raise NotImplementedError()

    @property
    def evaluate(self):
        """
        Raises a NotImplementedError() when
        trying to evaluate a UnaryNode.
        """

        raise NotImplementedError()

    
 