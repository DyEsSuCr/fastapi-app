from fastapi_mail import FastMail, ConnectionConfig
from pathlib import Path

from src.settings import settings

BASE_DIR = Path(__file__).resolve().parent

TEMPLATE_FOLDER = BASE_DIR.parent / 'static' / 'templates'

if not TEMPLATE_FOLDER.exists():
    raise FileNotFoundError(f'Template folder not found: {TEMPLATE_FOLDER}')

mail_config = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=settings.USE_CREDENTIALS,
    VALIDATE_CERTS=settings.VALIDATE_CERTS,
    TEMPLATE_FOLDER=str(TEMPLATE_FOLDER),
)

mail = FastMail(config=mail_config)
