import pytest
from app.main import app
from litestar.testing import TestClient

@pytest.fixture
async def client():
    test_client = TestClient(app=app)
    yield test_client