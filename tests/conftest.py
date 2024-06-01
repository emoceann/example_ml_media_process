import asyncio

import pytest
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from sqlalchemy import text, NullPool
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker

from src.core.settings import get_settings
from src.core.tasks.broker import get_broker
from src.server.app import get_app


settings = get_settings()


@pytest.fixture(scope="session")
async def get_session_maker():
    engine: AsyncEngine = create_async_engine(
        url=f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}/{settings.POSTGRES_DB}",
        echo=True,
        echo_pool=True,
        poolclass=NullPool
    )
    session_maker = async_sessionmaker(bind=engine, autocommit=False, autoflush=False)
    return session_maker


@pytest.fixture(scope="session")
async def get_db_session(get_session_maker):
    async with get_session_maker() as session:
        yield session


@pytest.fixture(scope="session", autouse=True)
async def prepare_db(get_db_session):
    await get_db_session.execute(text(
        "CREATE TABLE processed_data (id bigserial primary key, data jsonb,result_id varchar(36));"
    ))
    await get_db_session.execute(text(
        "CREATE INDEX request_idx ON processed_data(result_id);"
    ))
    await get_db_session.commit()
    yield
    await get_db_session.execute(
        text("DROP TABLE processed_data;")
    )
    await get_db_session.commit()


@pytest.fixture(scope="session")
def app() -> FastAPI:
    return get_app()


@pytest.fixture(scope="session")
async def client(app) -> AsyncClient:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client


@pytest.fixture(scope='session', autouse=True)
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
