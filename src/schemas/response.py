import uuid

from pydantic import BaseModel, ConfigDict
from src.schemas.book import CreateBookModel


class BookResponse(CreateBookModel):
    id: uuid.UUID
    model_config = ConfigDict(
        from_attributes=True
    )


class BookResponseList(BaseModel):
    books: list[BookResponse]
    model_config = ConfigDict(
        from_attributes=True
    )
