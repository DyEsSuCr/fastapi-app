from starlette import status


class BaseCustomException(Exception):
    """Base class for all custom exceptions"""

    status_code: int = status.HTTP_400_BAD_REQUEST
    message: str = 'An error occurred'
    error_code: str = 'error'

    def __init__(self, detail: str = None):
        self.detail = detail or self.message


class InvalidToken(BaseCustomException):
    """User has provided an invalid token"""

    status_code = status.HTTP_401_UNAUTHORIZED
    message = 'Invalid token'
    error_code = 'invalid_token'


class RevokedToken(BaseCustomException):
    """User has provided a token that has been revoked"""

    status_code = status.HTTP_401_UNAUTHORIZED
    message = 'Token has been revoked'
    error_code = 'revoked_token'


class AccessTokenRequired(BaseCustomException):
    """User has provided a refresh token when an access token is needed"""

    status_code = status.HTTP_401_UNAUTHORIZED
    message = 'Access token required'
    error_code = 'access_token_required'


class RefreshTokenRequired(BaseCustomException):
    """User has provided an access token when a refresh token is needed"""

    status_code = status.HTTP_401_UNAUTHORIZED
    message = 'Refresh token required'
    error_code = 'refresh_token_required'


class UserAlreadyExists(BaseCustomException):
    """User has provided an email for a user who exists during sign up."""

    status_code = status.HTTP_400_BAD_REQUEST
    message = 'User already exists'
    error_code = 'user_already_exists'


class InvalidCredentials(BaseCustomException):
    """User has provided wrong email or password during log in."""

    status_code = status.HTTP_401_UNAUTHORIZED
    message = 'Invalid credentials'
    error_code = 'invalid_credentials'


class InsufficientPermission(BaseCustomException):
    """User does not have the neccessary permissions to perform an action."""

    status_code = status.HTTP_403_FORBIDDEN
    message = 'Insufficient permissions'
    error_code = 'insufficient_permissions'


class UserNotFound(BaseCustomException):
    """User Not found"""

    status_code = status.HTTP_404_NOT_FOUND
    message = 'User not found'
    error_code = 'user_not_found'


class AccountNotVerified(BaseCustomException):
    """User account not verified"""

    status_code = status.HTTP_400_BAD_REQUEST
    message = 'Account not verified'
    error_code = 'account_not_verified'


class PasswordNotMatch(BaseCustomException):
    """Password does not match"""

    status_code = status.HTTP_400_BAD_REQUEST
    message = 'Password does not match'
    error_code = 'password_not_match'
