import uuid
from datetime import datetime
from pydantic import BaseModel, Field


class UserCreateModel(BaseModel):
    first_name: str = Field(max_length=25)
    last_name: str = Field(max_length=25)
    username: str = Field(max_length=8)
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)

    model_config = {
        'json_schema_extra': {
            'example': {
                'first_name': 'dylan',
                'last_name': 'suarez',
                'username': 'dyessucr',
                'email': 'dylan@gmail.com',
                'password': 'password123',
            }
        }
    }


class UserModel(BaseModel):
    uid: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool
    password_hash: str = Field(exclude=True)
    created_at: datetime
    update_at: datetime


class UserLoginModel(BaseModel):
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)
