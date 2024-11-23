from enum import Enum
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel
from fastapi import Query


class Pagination(BaseModel):
    page_number: Annotated[int, Query(ge=0)] = 0
    page_size: Annotated[int, Query(ge=1)] = 20


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