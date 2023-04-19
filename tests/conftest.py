import asyncio
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src import Base
from src.main import app

CONNECTION_URL = 'postgresql+asyncpg://app_test:testpostgres@localhost:5433/app_test'

pytest_plugins = [
    'tests.fixtures.utils',
    'tests.fixtures.routers',
]


@pytest.fixture(scope='session')
def event_loop(request) -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session', autouse=True)
async def async_session():
    engine_test = create_async_engine(CONNECTION_URL, echo=False)
    async_session_maker = async_sessionmaker(engine_test, expire_on_commit=False)

    async with async_session_maker() as session:
        async with engine_test.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        yield session

    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine_test.dispose()


@pytest_asyncio.fixture(scope='session')
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://testproducts') as client:
        yield client
