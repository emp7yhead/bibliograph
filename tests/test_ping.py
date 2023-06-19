import pytest
from fastapi.testclient import TestClient

from app.main import app

test_client = TestClient(app)


@pytest.mark.asyncio
async def test_ping():
    response = test_client.get("/ping")
    assert response.status_code == 200
    assert response.json() == "pong"
