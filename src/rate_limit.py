from slowapi import Limiter
from slowapi.util import get_remote_address

from .settings import settings


limiter = Limiter(key_func=get_remote_address, enabled=settings.ENABLE_RATE_LIMIT)
