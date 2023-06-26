import pytest
from tests.conftest import client


@pytest.mark.asyncio
async def test_index():
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == "Welcome to Bibliograph. Please go to /docs for more information."


@pytest.mark.asyncio
async def test_ping():
    response = await client.get("/ping")
    assert response.status_code == 200
    assert response.json() == "pong"


