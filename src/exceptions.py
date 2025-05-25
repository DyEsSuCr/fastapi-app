from typing import Any, Callable
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI
from starlette import status
from sqlalchemy.exc import SQLAlchemyError


class BooklyException(Exception):
    """This is the base class for all bookly errors"""

    pass


def create_exception_handler(
    status_code: int, initial_detail: Any
) -> Callable[[Request, Exception], JSONResponse]:
    async def exception_handler(request: Request, exc: BooklyException):
        return JSONResponse(content=initial_detail, status_code=status_code)

    return exception_handler


exception_responses = {
    BooklyException: {
        'status_code': status.HTTP_400_BAD_REQUEST,
        'message': 'Bad request',
        'error_code': 'bad_request',
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
