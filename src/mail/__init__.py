from fastapi_mail import MessageSchema, MessageType
from .config import mail


async def send_email(recipients: list[str], subject: str, body: str):
    message = MessageSchema(
        subject=subject,
        recipients=recipients,
        template_body={
            'subject': subject,
            'body': body,
        },
        subtype=MessageType.html,
    )

    await mail.send_message(message, template_name='email_template.html')
