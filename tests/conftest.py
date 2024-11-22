import asyncio
import os
import sys

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from src.core.config import settings

from main import app
from src.models.books import Book
from sqlalchemy.orm import sessionmaker

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)


@pytest_asyncio.fixture(name='client')
def client():
    cli = TestClient(app)
    return cli


# @pytest.fixture(scope='session')
# def event_loop():
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     yield loop
#     loop.close()


@pytest_asyncio.fixture()
async def test_engine():
    dsn = f'postgresql+asyncpg://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}'
    engine = create_async_engine(dsn, echo=True)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture()
async def test_async_session(test_engine):
    async_session = sessionmaker(
        bind=test_engine,
        class_=AsyncSession,
        autocommit=False,
        autoflush=False,
    )
    yield async_session


@pytest_asyncio.fixture()
async def db_session(test_async_session):
    async with test_async_session() as session:
        yield session


@pytest_asyncio.fixture(name='create_book')
async def create_book(db_session):
    async def inner(values):
        return await Book.add(db_session, **values)

    return inner


@pytest_asyncio.fixture(name='del_book')
async def del_book(db_session):
    async def inner(book_id):
        await Book.remove(db_session, book_id)
    return inner


values1 = {
    'title': 'Триумфальная арка',
    'author': "Э.М. Ремарк",
    'year': 1932,
    'status': "выдана",
}

values2 = {
    'title': 'Три товарища',
    'author': "Э.М. Ремарк",
    'year': 1929,
    'status': "выдана",
}

