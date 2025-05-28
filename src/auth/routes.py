from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi.responses import JSONResponse
from starlette import status

from src.database import DbSession
from src.database.redis import add_jti_to_blocklist

from .dependencies import (
    AccessTokenBearer,
    RefreshTokenBearer,
    RoleChecker,
    get_current_user,
)
from .schemas import (
    UserCreateModel,
    UserLoginModel,
    UserModel,
)
from .service import user_service
from .utils import (
    create_access_token,
    create_url_safe_token,
    decode_url_safe_token,
    verify_password,
)
from src.exceptions import (
    UserAlreadyExists,
    InvalidCredentials,
    InvalidToken,
    UserNotFound,
    AccountNotVerified,
)
from src.mail import send_email
from src.settings import settings

auth_router = APIRouter()
role_checker = RoleChecker(['admin', 'user'])


@auth_router.post('/signup', status_code=status.HTTP_201_CREATED)
async def create_user_account(
    user_data: UserCreateModel,
    bg_tasks: BackgroundTasks,
    session: DbSession,
):
    email = user_data.email

    user_exists = await user_service.user_exists(email, session)

    if user_exists:
        raise UserAlreadyExists()

    new_user = await user_service.create_user(user_data, session)

    token = create_url_safe_token({'email': email})

    link = f'{settings.DOMAIN_APP}/auth/verify/{token}'

    html = f"""
    <h1>Verify your Email</h1>
    <p>Please click this <a href="{link}">link</a> to verify your email</p>
    """

    subject = 'Verify Your email'

    bg_tasks.add_task(send_email, [email], subject, html)

    return {
        'message': 'Account Created! Check email to verify your account',
        'user': new_user,
        'link': link,
    }


@auth_router.get('/verify/{token}')
async def verify_user_account(token: str, session: DbSession):
    token_data = decode_url_safe_token(token)

    user_email = token_data.get('email')

    if user_email:
        user = await user_service.get_user_by_email(user_email, session)

        if not user:
            raise UserNotFound()

        await user_service.update_user(user, {'is_verified': True}, session)

        return JSONResponse(
            content={'message': 'Account verified successfully'},
            status_code=status.HTTP_200_OK,
        )

    return JSONResponse(
        content={'message': 'Error occured during verification'},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


@auth_router.post('/login')
async def login_users(login_data: UserLoginModel, session: DbSession):
    email = login_data.email
    password = login_data.password

    user = await user_service.get_user_by_email(email, session)

    if not user.is_verified:
        raise AccountNotVerified()

    if user is not None:
        password_valid = verify_password(password, user.password_hash)

        if password_valid:
            access_token = create_access_token(
                user_data={
                    'email': user.email,
                    'user_uid': str(user.uid),
                    'role': user.role,
                }
            )

            refresh_token = create_access_token(
                user_data={'email': user.email, 'user_uid': str(user.uid)},
                refresh=True,
                expiry=timedelta(days=settings.REFRESH_TOKEN_EXPIRY_DAYS),
            )

            return JSONResponse(
                content={
                    'message': 'Login successful',
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'user': {'email': user.email, 'uid': str(user.uid)},
                }
            )

    raise InvalidCredentials()


@auth_router.get('/refresh_token')
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details['exp']

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(user_data=token_details['user'])

        return JSONResponse(content={'access_token': new_access_token})

    raise InvalidToken


@auth_router.get('/me', response_model=UserModel)
async def get_current_user(
    user=Depends(get_current_user),
    _: bool = Depends(role_checker),
):
    return user


@auth_router.get('/logout')
async def revoke_token(token_details: dict = Depends(AccessTokenBearer())):
    jti = token_details['jti']

    await add_jti_to_blocklist(jti)

    return JSONResponse(
        content={'message': 'Logged Out Successfully'}, status_code=status.HTTP_200_OK
    )
