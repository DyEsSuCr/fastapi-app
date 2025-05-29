from typing import Any, Callable
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI
from starlette import status
from sqlalchemy.exc import SQLAlchemyError


class BaseException(Exception):
    """This is the base class for all bookly errors"""

    pass


class InvalidToken(BaseException):
    """User has provided an invalid or expired token"""

    pass


class RevokedToken(BaseException):
    """User has provided a token that has been revoked"""

    pass


class AccessTokenRequired(BaseException):
    """User has provided a refresh token when an access token is needed"""

    pass


class RefreshTokenRequired(BaseException):
    """User has provided an access token when a refresh token is needed"""

    pass


class UserAlreadyExists(BaseException):
    """User has provided an email for a user who exists during sign up."""

    pass


class InvalidCredentials(BaseException):
    """User has provided wrong email or password during log in."""

    pass


class InsufficientPermission(BaseException):
    """User does not have the neccessary permissions to perform an action."""

    pass


class UserNotFound(BaseException):
    """User Not found"""

    pass


class AccountNotVerified(BaseException):
    """User account not verified"""

    pass


class PasswordNotMatch(BaseException):
    """Password does not match"""

    pass


def create_exception_handler(
    status_code: int, initial_detail: Any
) -> Callable[[Request, Exception], JSONResponse]:
    async def exception_handler(request: Request, exc: BaseException):
        return JSONResponse(content=initial_detail, status_code=status_code)

    return exception_handler


exception_responses = {
    BaseException: {
        'status_code': status.HTTP_400_BAD_REQUEST,
        'message': 'Bad request',
        'error_code': 'bad_request',
    },
    InvalidToken: {
        'status_code': status.HTTP_401_UNAUTHORIZED,
        'message': 'Invalid token',
        'error_code': 'invalid_token',
    },
    RevokedToken: {
        'status_code': status.HTTP_401_UNAUTHORIZED,
        'message': 'Token has been revoked',
        'error_code': 'revoked_token',
    },
    AccessTokenRequired: {
        'status_code': status.HTTP_401_UNAUTHORIZED,
        'message': 'Access token required',
        'error_code': 'access_token_required',
    },
    RefreshTokenRequired: {
        'status_code': status.HTTP_401_UNAUTHORIZED,
        'message': 'Refresh token required',
        'error_code': 'refresh_token_required',
    },
    UserAlreadyExists: {
        'status_code': status.HTTP_400_BAD_REQUEST,
        'message': 'User already exists',
        'error_code': 'user_already_exists',
    },
    InvalidCredentials: {
        'status_code': status.HTTP_401_UNAUTHORIZED,
        'message': 'Invalid credentials',
        'error_code': 'invalid_credentials',
    },
    InsufficientPermission: {
        'status_code': status.HTTP_403_FORBIDDEN,
        'message': 'Insufficient permissions',
        'error_code': 'insufficient_permissions',
    },
    UserNotFound: {
        'status_code': status.HTTP_404_NOT_FOUND,
        'message': 'User not found',
        'error_code': 'user_not_found',
    },
    AccountNotVerified: {
        'status_code': status.HTTP_400_BAD_REQUEST,
        'message': 'Account not verified',
        'error_code': 'account_not_verified',
    },
    PasswordNotMatch: {
        'status_code': status.HTTP_400_BAD_REQUEST,
        'message': 'Password does not match',
        'error_code': 'password_not_match',
    },
}


def register_exceptions(app: FastAPI):
    for exception, response in exception_responses.items():
        app.add_exception_handler(
            exception,
            create_exception_handler(
                status_code=response['status_code'],
                initial_detail={
                    'message': response['message'],
                    'error_code': response['error_code'],
                },
            ),
        )

    @app.exception_handler(500)
    async def internal_server_error(request, exc):
        return JSONResponse(
            content={
                'message': 'Oops! Something went wrong',
                'error_code': 'server_error',
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    @app.exception_handler(SQLAlchemyError)
    async def database__error(request, exc):
        print(str(exc))
        return JSONResponse(
            content={
                'message': 'Oops! Something went wrong',
                'error_code': 'server_error',
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
