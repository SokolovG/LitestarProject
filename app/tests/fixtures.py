import pytest

from litestar.testing import TestClient

from app.main import app


@pytest.fixture
async def client():
    test_client = TestClient(app=app)
    yield test_client