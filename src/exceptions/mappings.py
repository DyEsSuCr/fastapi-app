from starlette import status
from sqlalchemy.exc import SQLAlchemyError
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .custom_exceptions import (
    InvalidToken,
    RevokedToken,
    AccessTokenRequired,
    RefreshTokenRequired,
    UserAlreadyExists,
    InvalidCredentials,
    InsufficientPermission,
    UserNotFound,
    AccountNotVerified,
    PasswordNotMatch,
)
from .handlers import create_exception_handler

exception_responses = {
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
    async def internal_server_error(request: Request, exc: Exception):
        return JSONResponse(
            content={
                'message': 'Oops! Something went wrong',
                'error_code': 'server_error',
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    @app.exception_handler(SQLAlchemyError)
    async def database_error(request: Request, exc: SQLAlchemyError):
        print(str(exc))
        return JSONResponse(
            content={
                'message': 'Oops! Something went wrong',
                'error_code': 'server_error',
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
