import pytest
import os
import sys
from dotenv import load_dotenv


load_dotenv('.env.sample')

from fastapi.testclient import TestClient

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from main import app
from src.core.config import Settings


settings = Settings()


@pytest.fixture(name='client')
def client():
    cli = TestClient(app)
    return cli


