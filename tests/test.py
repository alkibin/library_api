import sys
import os
from fastapi import status

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)


def test_add_book(client):
    params = {
        'title': 'На западном фронте без перемен',
        'author': "Э.М. Ремарк",
        'year': 1928,
        'status': "выдана"
    }

    response = client.post('/api/v1//book_manager/create', json=params)

    assert response.status_code == status.HTTP_200_OK