import logging
import uuid
from jose import jwt, JWTError
from itsdangerous import URLSafeTimedSerializer
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
        claims=payload,
        key=settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )

    return token


def decode_token(token: str) -> dict:
    try:
        token_data = jwt.decode(
            token=token,
            key=settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return token_data

    except JWTError as e:
        logging.exception('Token decoding failed', exc_info=e)
        return None


serializer = URLSafeTimedSerializer(
    secret_key=settings.JWT_SECRET_KEY, salt='email-configuration'
)


def create_url_safe_token(data: dict):
    token = serializer.dumps(data)

    return token


def decode_url_safe_token(token: str):
    try:
        token_data = serializer.loads(token)

        return token_data

    except Exception as e:
        logging.error(str(e))
