import pytest
from .fixtures import client


@pytest.mark.asyncio
async def test_get_users_empty_list(client):
    response = client.get('/users')
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0

