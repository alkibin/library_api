import uuid

from sqlalchemy import Column, Integer, String, insert, select, update, and_, or_, delete, func
from sqlalchemy import Enum as SqlAlchemyEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.base import Base
from src.schemas.book import BookStatusEnum


class Book(Base):
    __tablename__ = 'book'
    __table_args__ = {'schema': 'book_library'}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    author = Column(String)
    year = Column(Integer)
    status = Column(SqlAlchemyEnum(BookStatusEnum))

    @classmethod
    async def add(cls, session: AsyncSession, **values):
        stmt = insert(cls).values(**values).returning(cls)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @classmethod
    async def remove(cls, session: AsyncSession, book_id):
        stmt = delete(cls).where(cls.id == book_id).returning(cls)
        result = await session.execute(stmt)
        return result.scalars().one_or_none()

    @classmethod
    async def get_books_by_option(cls, session: AsyncSession, title=None, author=None, year=None):
        options = []
        if title:
            options.append(func.lower(cls.title).like(f"%{title.lower()}%"))
        if author:
            options.append(func.lower(cls.author).like(f"%{author.lower()}%"))
        if year:
            options.append(cls.year == year)

        query = select(cls)
        if options:
            query = query.filter(or_(*options))
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def find_book(cls, session: AsyncSession, title, author, year):
        query = (
            select(cls)
            .where(
                and_(
                    cls.title == title,
                    cls.author == author,
                    cls.year == year,
                )
            )
        )
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def get_all_books(cls, session: AsyncSession, pagination):
        query = select(cls).limit(pagination.page_size).offset(pagination.page_number)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def update_status(cls, session, status, book_id):
        stmt = update(cls).where(cls.id == book_id).values(status=status).returning(cls)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()
