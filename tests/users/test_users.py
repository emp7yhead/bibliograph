import pytest
from app.auth.jwthandler import create_access_token

from tests.conftest import client


# NOTE: rework it
@pytest.mark.asyncio
async def test_empty_users():
    response = await client.get("/users")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_user():
    """Register user and check that that username cannot be used again."""
    response = await client.post(
            "/register",
            json={
                'email': 'test@test.com',
                'username': 'test',
                'password': 'test'
            },
            headers={"content-type": "application/json"}
        )
    assert response.status_code == 201
    test_json = response.json()
    assert test_json['username'] == 'test'
    assert test_json['email'] == 'test@test.com'

    response = await client.post(
            "/register",
            json={
                'email': 'test@test.com',
                'username': 'test',
                'password': 'test'
            },
            headers={"content-type": "application/json"}
        )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_login_user():
    """Login user and check that status code is success."""
    response = await client.post(
            "/login",
            data={
                'username': 'test',
                'password': 'test'
            },
            headers={"content-type": "application/x-www-form-urlencoded"}
        )
    assert response.is_success


@pytest.mark.asyncio
async def test_update_user():
    """Update user and check that he is changed."""
    user_access_token = create_access_token({"sub": "test"})
    response = await client.put(
            "/users/1",
            json={
                'email': 'test1@test.com',
                'username': 'test1',
                'password': 'test1'
            },
            headers={"content-type": "application/json", 'Authorization': f'Bearer {user_access_token}'},
        )
    assert response.is_success
    response = await client.get(
            "/users/1",
    )
    assert response.status_code == 200
    test_json = response.json()
    assert test_json['username'] == 'test1'
    assert test_json['email'] == 'test1@test.com'


# @pytest.mark.asyncio
# async def test_delete_user():
#     """Delete user and check that he is deleted."""
#     user_access_token = create_access_token({"sub": "test1"})
#     response = await client.delete(
#             "/users/1",
#             headers={'Authorization': f'Bearer {user_access_token}'}
#         )
#     assert response.is_success
#     response = await client.get("/users")
#     assert response.json() == []
