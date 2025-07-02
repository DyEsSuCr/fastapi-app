from fastapi_mail import MessageSchema, MessageType
from asgiref.sync import async_to_sync
from celery import Celery

from src.mail import mail
from src.settings import settings

c_app = Celery()

c_app.conf.update(
    broker_url=settings.REDIS_URL,
    result_backend=settings.REDIS_URL,
    broker_connection_retry_on_startup=True,
)


@c_app.task()
def send_email(recipients: list[str], subject: str, body: str):
    message = MessageSchema(
        subject=subject,
        recipients=recipients,
        template_body={
            'subject': subject,
            'body': body,
        },
        subtype=MessageType.html,
    )

    async_to_sync(mail.send_message)(message, template_name='email_template.html')
