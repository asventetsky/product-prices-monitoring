"""Exception raised for errors during request handling."""


class LambdaException(Exception):

    """
    Attributes:
        message -- explanation of the exception
    """

    def __init__(self, message="Lambda exception"):
        self.message = message
        super().__init__(self.message)
