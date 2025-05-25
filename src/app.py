from fastapi import FastAPI

from src.settings import settings
from .logging import configure_logging, LogLevels


configure_logging(LogLevels.info)

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
)


@app.get('/')
async def root():
    return {'message': f'FastAPI app running in {settings.ENVIRONMENT} mode'}
