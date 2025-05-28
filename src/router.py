from fastapi import FastAPI

from src.auth.routes import auth_router


def register_routes(app: FastAPI):
    app.include_router(auth_router, prefix='/auth', tags=['auth'])
