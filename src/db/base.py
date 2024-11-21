from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

from src.core.config import settings

Base: DeclarativeMeta = declarative_base()
Base.metadata.schema = 'book_library'
DATABASE_URL = f'postgresql+asyncpg://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}'
engine = create_async_engine(DATABASE_URL, echo=False, future=True)
