class TokenExpiredException(Exception):
    """
    Exception raised when an authentication token has expired.
    
    Attributes:
        message (str): Explanation of the error. 
            Defaults to "Token has expired. Please re-authenticate."
    """
    def __init__(self, message="Token has expired. Please re-authenticate."):
        super().__init__(message)

class RefreshTokenExpiredException(Exception):
    """
    Exception raised when a refresh token has expired.

    Attributes:
        message (str): Explanation of the error. 
            Defaults to "Refresh token has expired. Please re-authenticate."
    """
    def __init__(self, message="Refresh token has expired. Please re-authenticate."):
        super().__init__(message)

class InvalidTokenException(Exception):
    """
    Exception raised when an authentication token is invalid.

    Attributes:
        message (str): Explanation of the error. 
            Defaults to "Token is invalid. Please re-authenticate."
    """
    def __init__(self, message="Token is invalid. Please re-authenticate."):
        super().__init__(message)
