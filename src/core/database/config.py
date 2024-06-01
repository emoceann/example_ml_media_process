from functools import cache
from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from src.core.settings import get_settings

settings = get_settings()


@cache
def get_engine() -> AsyncEngine:
    general_engine: AsyncEngine = create_async_engine(
        url=f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}/{settings.POSTGRES_DB}",
        echo=True,
        echo_pool=True
    )
    return general_engine


@cache
def get_session_maker(engine: AsyncEngine = Depends(get_engine)) -> async_sessionmaker[AsyncSession]:
    session_maker = async_sessionmaker(bind=engine, autocommit=False, autoflush=False)
    return session_maker


async def get_session(
        session_maker: async_sessionmaker[AsyncSession] = Depends(get_session_maker)
) -> AsyncGenerator[AsyncSession, None]:
    async with session_maker() as session:
        yield session
