import uvicorn
from src.settings import settings


if __name__ == '__main__':
    uvicorn.run(
        'src.app:app',
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=settings.ENVIRONMENT == 'dev',
    )
