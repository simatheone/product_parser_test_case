import asyncio
import pytest
from typing import AsyncGenerator, Generator

import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src import Base
from src.dependencies import get_async_session
from src.main import app

CONNECTION_URL = 'postgresql+asyncpg://app_test:testpostgres@localhost:5433/app_test'

engine_test = create_async_engine(CONNECTION_URL, echo=False)
async_session_maker = async_sessionmaker(engine_test, expire_on_commit=False)


pytest_plugins = [
    'tests.fixtures.utils',
]


@pytest.fixture(scope='session')
def event_loop(request) -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session', autouse=True)
async def init_test_db():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def async_session_test() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_async_session] = async_session_test


@pytest_asyncio.fixture(scope='session')
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://testproducts') as client:
        yield client
