import os

import pytest_asyncio
from dotenv import load_dotenv
from httpx import AsyncClient as Client
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

load_dotenv(".env.test")

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

BASE_URL = "http://api:8000/"


@pytest_asyncio.fixture(name='client')
async def client():
    async with Client(base_url=BASE_URL) as ac:
        yield ac


@pytest_asyncio.fixture()
async def test_engine():
    dsn = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
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
        result = await db_session.execute(
            text(
                """
                    INSERT INTO book_library.book (id, title, author, year, status)
                    VALUES(:id, :title, :author, :year, :status)
                    RETURNING id; 
                """
            ), values
        )
        await db_session.commit()
        return result.scalar_one_or_none()

    return inner


@pytest_asyncio.fixture(name='del_book')
async def del_book(db_session):
    async def inner(book_id):
        result = await db_session.execute(
            text(
                """
                    DELETE FROM book_library.book
                    WHERE id = :book_id;
                """
            ), {'book_id': book_id}
        )
        await db_session.commit()

    return inner


values = {
    'title': 'Магия утра',
    'author': 'Эл Род',
    'year': 2018,
    'status': 'BORROWED'
}
