import uuid
from http import HTTPStatus

import pytest
from faker import Faker

from conftest import values

faker = Faker()


@pytest.mark.asyncio
async def test_add_book(client, del_book):
    params = dict(
        title=faker.text(max_nb_chars=20),
        author=faker.name(),
        year=int(faker.year())
    )
    response = await client.post('api/v1/book_manager/create', json=params)

    assert response.status_code == HTTPStatus.CREATED

    book = response.json()
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
async def test_get_book(client, create_book, del_book, title, author, year, expected):
    book_id = uuid.uuid4()
    values['id'] = book_id
    await create_book(values)

    params = {
        'title': title,
        'author': author,
        'year': year,
    }
    response = await client.get('api/v1/book_manager/get-book', params=params)

    await del_book(book_id)
    assert response.status_code == expected


@pytest.mark.parametrize(
    "page_number, page_size, expected",
    [
        (0, 20, HTTPStatus.OK),
        (0, 100, HTTPStatus.OK),
        (0, 0, HTTPStatus.UNPROCESSABLE_ENTITY)
    ]
)
@pytest.mark.asyncio
async def test_show_books(client, page_number, page_size, expected):
    params = {
        'page_number': page_number,
        'page_size': page_size
    }
    response = await client.get('api/v1/book_manager/show-all', params=params)
    assert response.status_code == expected


@pytest.mark.parametrize(
    'new_status, expected',
    [
        ('выдана', HTTPStatus.OK),
        ('в наличии', HTTPStatus.OK),
        ('не доступен', HTTPStatus.UNPROCESSABLE_ENTITY),
    ]
)
@pytest.mark.asyncio
async def test_change_status(client, create_book, del_book, new_status, expected):
    book_id = uuid.uuid4()
    values['id'] = book_id
    await create_book(values)

    params = {
        'book_id': str(book_id),
        'status': new_status
    }
    response = await client.post('api/v1/book_manager/change-status', json=params)
    await del_book(book_id)

    assert response.status_code == expected


@pytest.mark.asyncio
async def test_delete_book(client, create_book):
    book_id = uuid.uuid4()
    values['id'] = book_id
    await create_book(values)

    response = await client.delete(f'api/v1/book_manager/delete/{book_id}')
    assert response.status_code == HTTPStatus.NO_CONTENT

    response = await client.delete(f'api/v1/book_manager/delete/{book_id}')
    assert response.status_code == HTTPStatus.NOT_FOUND
