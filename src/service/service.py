from fastapi import Depends

from src.models.books import Book
from src.db.session import AsyncSession, get_session


class BookService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_book(self, params):
        find = await Book.find_book(self.session, **params.model_dump(exclude=['status']))
        if not find:
            return await Book.add(self.session, **params.model_dump())

    async def book_delete(self, book_id):
        return await Book.remove(self.session, book_id)

    async def book_find(self, options):
        option = {k: v for k, v in options.model_dump().items() if v is not None}
        return await Book.get_books_by_option(self.session, **option)

    async def show_books(self, pagination):
        return await Book.get_all_books(self.session, pagination)

    async def change_status(self, new_status):
        return await Book.update_status(self.session, **new_status.model_dump())


def get_book_manager(session=Depends(get_session)):
    return BookService(session)
