import asyncio
import time
from typing import TYPE_CHECKING, Generator, AsyncGenerator

import pytest_asyncio
import sqlalchemy as sa
from httpx import AsyncClient
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession

from db_models.db_models import metadata, Base
from shop_be.app import create_app
from shop_be.conf.db import session_factory, async_session
from shop_be.conf.settings import Settings, settings

if TYPE_CHECKING:
    from asyncio import AbstractEventLoop
    from fastapi import FastAPI


async def _create_test_db(engine: 'AsyncEngine', new_db_name: str):
    async with engine.connect() as conn:
        conn = await conn.execution_options(isolation_level='AUTOCOMMIT')
        await conn.execute(sa.text('DROP DATABASE IF EXISTS %s' % new_db_name))
        await conn.execute(sa.text('CREATE DATABASE %s' % new_db_name))


async def _drop_test_db(engine: 'AsyncEngine', new_db_name: str):
    async with engine.connect() as conn:
        conn = await conn.execution_options(isolation_level='AUTOCOMMIT')
        await conn.execute(sa.text('DROP DATABASE %s' % new_db_name))


@pytest_asyncio.fixture(scope='session')
def test_db_name() -> str:
    return f'harvest_hub_tests_{int(time.time())}'


@pytest_asyncio.fixture(scope='session')
def test_settings(test_db_name: str) -> Settings:
    return Settings(DB_NAME=test_db_name)


@pytest_asyncio.fixture(scope='session')
async def sync_engine(test_settings: Settings) -> AsyncGenerator:
    test_settings.DB_DRIVER = 'postgresql'
    engine = create_engine(url=test_settings.sqlalchemy_database_uri)
    test_settings.DB_DRIVER = 'postgresql+asyncpg'
    session_factory.configure(bind=engine)
    yield engine


@pytest_asyncio.fixture(scope='session', autouse=True)
async def init_test_db(
        test_settings: Settings,
        test_db_name: str,
        sync_engine: Engine,
) -> AsyncGenerator[None, None]:
    conn_url = settings.sqlalchemy_database_uri
    engine = create_async_engine(conn_url)
    await _create_test_db(engine, test_db_name)
    test_engine = create_async_engine(test_settings.sqlalchemy_database_uri)
    async with test_engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

    yield

    sync_engine.dispose()
    await test_engine.dispose()
    if metadata.bind:
        await metadata.bind.dispose()
    await _drop_test_db(engine, test_db_name)


@pytest_asyncio.fixture(scope='session')
def app(test_settings: Settings) -> 'FastAPI':
    return create_app(test_settings)


@pytest_asyncio.fixture(scope='session')
async def async_db_session(app: 'FastAPI') -> AsyncGenerator['AsyncSession', None]:
    async with async_session() as session:
        # for factory_ in FACTORIES:
        #     factory_._meta.sqlalchemy_session = session

        yield session


@pytest_asyncio.fixture(scope='function', autouse=True)
async def clear_db(async_db_session: 'AsyncSession') -> AsyncGenerator[None, None]:
    yield

    await async_db_session.execute(text('TRUNCATE {} RESTART IDENTITY;'.format(
        ','.join(table.name
                 for table in reversed(Base.metadata.sorted_tables)))))
    await async_db_session.commit()


@pytest_asyncio.fixture(scope='session')
async def client(app: 'FastAPI') -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url=f'http://test/api/') as http_client:
        yield http_client


@pytest_asyncio.fixture(scope='session')
def event_loop() -> Generator['AbstractEventLoop', None, None]:
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()
