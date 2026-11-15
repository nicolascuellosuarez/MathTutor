class MathTutorError(Exception):
    """
    Base class for every exception in the app.
    """


class IncompleteExpressionError(MathTutorError):
    """
    Raised when the user inputs an incomplete expression.
    """


class InvalidOperationError(MathTutorError):
    """
    Raised when the user inputs an invalid operation.
    """


class UnboundVariableError(MathTutorError):
    """
    Raised when the user tries to evaluate a variable
    with no value.
    """
