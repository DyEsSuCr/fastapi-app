from fastapi import FastAPI

from src.settings import settings
from .middleware import register_middleware


app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
)


@app.get('/')
async def root():
    return {'message': f'FastAPI app running in {settings.ENVIRONMENT} mode'}


register_middleware(app)
