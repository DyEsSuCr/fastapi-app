import logging
import uuid
import jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext

from src.settings import settings

passwd_context = CryptContext(schemes=['bcrypt'])


def generate_passwd_hash(password: str) -> str:
    hash = passwd_context.hash(password)

    return hash


def verify_password(password: str, hash: str) -> bool:
    return passwd_context.verify(password, hash)


def create_access_token(
    user_data: dict, expiry: timedelta = None, refresh: bool = False
):
    payload = {}

    payload['user'] = user_data
    payload['exp'] = datetime.now(timezone.utc) + (
        expiry
        if expiry is not None
        else timedelta(seconds=settings.ACCESS_TOKEN_EXPIRY_SECONDS)
    )
    payload['jti'] = str(uuid.uuid4())

    payload['refresh'] = refresh

    token = jwt.encode(
        payload=payload,
        key=settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )

    return token


def decode_token(token: str) -> dict:
    try:
        token_data = jwt.decode(
            jwt=token, key=settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )

        return token_data

    except jwt.PyJWTError as e:
        logging.exception(e)
        return None
