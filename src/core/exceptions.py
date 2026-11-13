class MathTutorError(Exception):
    """
    Base class for every exception in the app.
    """

    pass

class IncompleteExpressionError(MathTutorError):
    """
    Raised when the user inputs an incomplete expression.
    """

    pass

class  InvalidOperationError(MathTutorError):
    """
    Raised when the user inputs an invalid operation.
    """

    pass