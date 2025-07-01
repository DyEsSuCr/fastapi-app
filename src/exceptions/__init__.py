from starlette import status
from sqlalchemy.exc import SQLAlchemyError
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .custom_exceptions import BaseCustomException


def register_exceptions(app: FastAPI):
    @app.exception_handler(BaseCustomException)
    async def handle_custom_exception(request: Request, exc: BaseCustomException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                'message': exc.detail,
                'error_code': exc.error_code,
            },
        )

    @app.exception_handler(SQLAlchemyError)
    async def handle_database_error(request: Request, exc: SQLAlchemyError):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                'message': 'Oops! Something went wrong',
                'error_code': 'server_error',
            },
        )

    @app.exception_handler(Exception)
    async def handle_unexpected_error(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                'message': 'Oops! Something went wrong',
                'error_code': 'server_error',
            },
        )
