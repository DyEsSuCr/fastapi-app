import redis.asyncio as aioredis

from src.settings import settings

token_blocklist = aioredis.from_url(
    settings.REDIS_URL, encoding='utf-8', decode_responses=True
)


async def add_jti_to_blocklist(jti: str) -> None:
    await token_blocklist.set(name=jti, value='', ex=settings.JTI_EXPIRY)


async def token_in_blocklist(jti: str) -> bool:
    jti = await token_blocklist.get(jti)

    return jti is not None
