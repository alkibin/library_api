from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator


class Pagination(BaseModel):
    offset: int
    limit: int


class BookStatusEnum(str, Enum):
    AVAILABLE = 'в наличии'
    BORROWED = 'выдана'


class CreateBookModel(BaseModel):
    title: str
    author: str
    year: int
    status: BookStatusEnum


class BookFindParams(BaseModel):
    title: str | None = None
    author: str | None = None
    year: int | None = None


class BookStatus(BaseModel):
    book_id: UUID
    status: BookStatusEnum