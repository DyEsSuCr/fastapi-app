from fastapi import FastAPI

from src.settings import settings
from .exceptions import register_exceptions
from .middleware import register_middleware
from .router import register_routes


app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
)


@app.get('/')
async def root():
    return {'message': f'FastAPI app running in {settings.ENVIRONMENT} mode'}


register_exceptions(app)
register_middleware(app)
register_routes(app)
