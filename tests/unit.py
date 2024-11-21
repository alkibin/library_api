import sys
import os
from fastapi import status
import pytest

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)


def test_add_book(client):
    params = {
        'title': 'На западном фронте без перемен',
        'author': "Э.М. Ремарк",
        'year': 1928,
        'status': "выдана"
    }
    response = client.post('/api/v1/book_manager/create', json=params)

    assert response.status_code == status.HTTP_200_OK

@pytest.mark.parametrize(
    "book_id,expected",
    [
        ('', status.HTTP_204_NO_CONTENT),
        ('', status.HTTP_400_BAD_REQUEST),
        ('', status.HTTP_400_BAD_REQUEST),
    ]
)
def test_delete_book(client, book_id, expected):
    params = {'book_id': book_id}
    response = client.delete(f'/api/v1/delete/{book_id}', params=params)
    assert response.status_code == expected

@pytest.mark.parametrize(
    "title,author,year,expected",
    [
        ('Триумфальная арка', 'Э.М. Ремарк', '1932', status.HTTP_200_OK),
        ('Триумфальная арка', 'Э.М. Ремарк', None, status.HTTP_200_OK),
        ('Триумфальная арка', None, None, status.HTTP_200_OK),
    ]
)
def test_get_book(client, title, author, year, expected):
    params = {
        'title': title,
        'author': author,
        'year': year,
    }
    response = client.get('/api/v1/get-book', params=params)

    assert response.status_code == expected


@pytest.mark.parametrize(
    "page_number,page_size,expected",
    [
        (0, 20, status.HTTP_200_OK),
        (10, 100, status.HTTP_200_OK),
        (-1, 4, status.HTTP_400_BAD_REQUEST),
        (0, -5, status.HTTP_400_BAD_REQUEST)
    ]
)
def test_show_books(client, page_number, page_size, expected):
    params ={
        'page_number': page_number,
        'page_size': page_size
    }
    response = client.get('/api/v1/book_manager/show-all',  params=params)
    assert response.status_code == expected


@pytest.mark.parametrize(
    'book_id,new_status,expected',
    ('', 'в наличии', status.HTTP_200_OK),
    ('', 'не доступен', status.HTTP_422_UNPROCESSABLE_ENTITY),
)
def test_change_status(client, book_id, new_status, expected):
    params = {
        'book_id': book_id,
        'status': new_status
    }
    response = client.post('/api/v1/change-status', json=params)
    assert response.status_code == expected