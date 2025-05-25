from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import Annotated, AsyncGenerator
from fastapi import Depends

from ..settings import settings


async_engine = create_async_engine(
    settings.DATABASE_URL, echo=settings.ENVIRONMENT == 'dev'
)

async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


DbSession = Annotated[AsyncSession, Depends(get_session)]
