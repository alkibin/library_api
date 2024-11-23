from random import choice
import uuid

from faker import Faker
from sqlalchemy import text

from src.db.base import Base, engine
from src.db.session import async_session
from src.models.books import Book


async def create_schema(engine):
    async with engine.begin() as conn:
        await conn.execute(text('CREATE SCHEMA IF NOT EXISTS book_library'))


async def init_db() -> None:
    await create_schema(engine)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def add_test_data() -> None:
    async with async_session() as session:
        faker = Faker()
        test_data = [
            Book(
                id=uuid.uuid4(),
                title=faker.text(max_nb_chars=20),
                author=faker.name(),
                year=int(faker.year()),
                status=choice(['в наличии', 'выдана'])
            ) for _ in range(100)
        ]
        session.add_all(test_data)
        await session.commit()
