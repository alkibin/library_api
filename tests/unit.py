import os
import sys

import pytest
from fastapi import status

from conftest import values1, values2

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)


async def test_add_book(client, del_book):
    params = {
        'title': 'На западном фронте без перемен',
        'author': "Э.М. Ремарк",
        'year': 1928,
        'status': "выдана"
    }
    response = client.post('/api/v1/book_manager/create', json=params)
    assert response.status_code == status.HTTP_201_CREATED

    book = response.json()
    book_id = book['id']
    await del_book(book_id)


@pytest.mark.parametrize(
    "title, author, year, expected",
    [
        ('Триумфальная арка', 'Э.М. Ремарк', 1932, status.HTTP_200_OK),
    ]
)
@pytest.mark.asyncio
async def test_get_book(client, create_book, del_book, title, author, year, expected):
    book = await create_book(values1)
    params = {
        'title': title,
        'author': author,
        'year': year,
    }
    response = client.get('/api/v1/book_manager/get-book', params=params)
    await del_book(book.id)
    assert response.status_code == expected


@pytest.mark.parametrize(
    "page_number, page_size, expected",
    [
        (0, 20, status.HTTP_200_OK),
    ]
)
def test_show_books(client, page_number, page_size, expected):
    params = {
        'page_number': page_number,
        'page_size': page_size
    }
    response = client.get('/api/v1/book_manager/show-all', params=params)
    assert response.status_code == expected


@pytest.mark.parametrize(
    'new_status, expected',
    [
        ('выдана', status.HTTP_200_OK),
        ('не доступен', status.HTTP_422_UNPROCESSABLE_ENTITY),
    ]
)
@pytest.mark.asyncio
async def test_change_status(client, create_book, del_book, new_status, expected):
    book = await create_book(values1)
    params = {
        'book_id': str(book.id),
        'status': new_status
    }
    response = client.post('/api/v1/book_manager/change-status', json=params)

    assert response.status_code == expected

    await del_book(book.id)


@pytest.mark.asyncio
async def test_delete_book(client, create_book):
    book = await create_book(values2)

    response = client.delete(f'/api/v1/book_manager/delete/{book.id}')

    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = client.delete(f'/api/v1/book_manager/delete/{book.id}')
    assert response.status_code == status.HTTP_404_NOT_FOUND