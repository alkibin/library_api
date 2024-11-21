from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from src.schemas.book import CreateBookModel, BookFindParams, Pagination, BookStatus
from src.schemas.response import BookResponse, BookResponseList
from src.service.service import get_book_manager, BookService

router = APIRouter(prefix='/api/v1/book_manager', tags=['manager'])


@router.post('/create', response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def add_book(
        params: CreateBookModel,
        service: BookService = Depends(get_book_manager)
):
    result = await service.add_book(params)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Такая книга уже есть в базе'
        )
    return result


@router.delete('/delete/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
        book_id: UUID,
        service: BookService = Depends(get_book_manager)
):
    result = await service.book_delete(book_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Удаляемая книга была удалена ранее или не существовала'
        )
    return result


@router.get('/get-book', response_model=BookResponseList, status_code=status.HTTP_200_OK)
async def get_book(
        params: BookFindParams = Depends(),
        service: BookService = Depends(get_book_manager)
):
    books = await service.book_find(params)
    if not books:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Искомой книги нет в базе'
        )
    return {'books': books}


@router.get('/show-all', response_model=BookResponseList, status_code=status.HTTP_200_OK)
async def show_books(
        pagination: Pagination = Depends(),
        service: BookService = Depends(get_book_manager)
):
    books = await service.show_books(pagination)
    return {'books': books}


@router.post('/change-status', response_model=BookResponse, status_code=status.HTTP_200_OK)
async def change_status(
        new_status: BookStatus,
        service: BookService = Depends(get_book_manager)
):
    return await service.change_status(new_status)
