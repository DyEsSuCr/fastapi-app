import uuid
from datetime import datetime
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    __tablename__ = 'users'

    uid: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    username: str
    email: str
    first_name: str
    last_name: str
    role: str = Field(default='user', nullable=False)
    is_verified: bool = Field(default=False)
    password_hash: str = Field(nullable=False, exclude=True)

    created_at: datetime = Field(default_factory=datetime.now)
    update_at: datetime = Field(default_factory=datetime.now)

    def __repr__(self):
        return f'<User {self.username}>'
