class BaseCustomException(Exception):
    """This is the base class for all bookly errors"""

    pass


class InvalidToken(BaseCustomException):
    """User has provided an invalid or expired token"""

    pass


class RevokedToken(BaseCustomException):
    """User has provided a token that has been revoked"""

    pass


class AccessTokenRequired(BaseCustomException):
    """User has provided a refresh token when an access token is needed"""

    pass


class RefreshTokenRequired(BaseCustomException):
    """User has provided an access token when a refresh token is needed"""

    pass


class UserAlreadyExists(BaseCustomException):
    """User has provided an email for a user who exists during sign up."""

    pass


class InvalidCredentials(BaseCustomException):
    """User has provided wrong email or password during log in."""

    pass


class InsufficientPermission(BaseCustomException):
    """User does not have the neccessary permissions to perform an action."""

    pass


class UserNotFound(BaseCustomException):
    """User Not found"""

    pass


class AccountNotVerified(BaseCustomException):
    """User account not verified"""

    pass


class PasswordNotMatch(BaseCustomException):
    """Password does not match"""

    pass
