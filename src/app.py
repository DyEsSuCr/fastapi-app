from fastapi import FastAPI, Request

from .settings import settings
from .exceptions import register_exceptions
from .middleware import register_middleware
from .router import register_routes
from .rate_limit import limiter


app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
)


@app.get('/')
@limiter.limit('1/second')
async def root(request: Request):
    return {'message': f'FastAPI app running in {settings.ENVIRONMENT} mode'}


register_exceptions(app)
register_middleware(app)
register_routes(app)
