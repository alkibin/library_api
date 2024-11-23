import os
import random
import sys
import uuid
from http import HTTPStatus

import pytest
from aiohttp import ClientSession
from faker import Faker

from conftest import values, BASE_URL

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

faker = Faker()


@pytest.mark.asyncio
async def test_add_book(del_book):
    params = dict(
        title=faker.text(max_nb_chars=20),
        author=faker.name(),
        year=int(faker.year())
    )
    async with ClientSession() as session:
        response = await session.post(f'{BASE_URL}api/v1/book_manager/create', json=params)

    assert response.status == HTTPStatus.CREATED

    book = await response.json()
    book_id = book['id']
    await del_book(book_id)


@pytest.mark.parametrize(
    "title, author, year, expected",
    [
        ('Триумфальная арка', 'Э.М. Ремарк', 1932, HTTPStatus.BAD_REQUEST),
        ('Триумфальная арка', 'Э.М. Ремарк', 1933, HTTPStatus.BAD_REQUEST),
        ('Магия утра', 'Эл Род', 2018, HTTPStatus.OK)
    ]
)
@pytest.mark.asyncio
async def test_get_book(create_book, del_book, title, author, year, expected):
    book_id = uuid.uuid4()
    values['id'] = book_id
    await create_book(values)

    params = {
        'title': title,
        'author': author,
        'year': year,
    }
    async with ClientSession() as session:
        response = await session.get(f'{BASE_URL}api/v1/book_manager/get-book', params=params)

        await del_book(book_id)
        assert response.status == expected


@pytest.mark.parametrize(
    "page_number, page_size, expected",
    [
        (0, 20, HTTPStatus.OK),
        (0, 100, HTTPStatus.OK),
        (0, 0, HTTPStatus.UNPROCESSABLE_ENTITY)
    ]
)
@pytest.mark.asyncio
async def test_show_books(page_number, page_size, expected):
    params = {
        'page_number': page_number,
        'page_size': page_size
    }
    async with ClientSession() as session:
        response = await session.get(f'{BASE_URL}api/v1/book_manager/show-all', params=params)
    assert response.status == expected


@pytest.mark.parametrize(
    'new_status, expected',
    [
        ('выдана', HTTPStatus.OK),
        ('в наличии', HTTPStatus.OK),
        ('не доступен', HTTPStatus.UNPROCESSABLE_ENTITY),
    ]
)
@pytest.mark.asyncio
async def test_change_status(create_book, del_book, new_status, expected):
    book_id = uuid.uuid4()
    values['id'] = book_id
    await create_book(values)

    params = {
        'book_id': str(book_id),
        'status': new_status
    }
    async with ClientSession() as session:
        response = await session.post(f'{BASE_URL}api/v1/book_manager/change-status', json=params)
    await del_book(book_id)

    assert response.status == expected


@pytest.mark.asyncio
async def test_delete_book(create_book):
    book_id = uuid.uuid4()
    values['id'] = book_id
    await create_book(values)
    async with ClientSession() as session:
        response = await session.delete(f'{BASE_URL}api/v1/book_manager/delete/{book_id}')
        assert response.status == HTTPStatus.NO_CONTENT

        response = await session.delete(f'{BASE_URL}api/v1/book_manager/delete/{book_id}')
        assert response.status == HTTPStatus.NOT_FOUND
