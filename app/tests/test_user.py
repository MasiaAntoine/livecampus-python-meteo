import pytest
import uuid
from httpx import AsyncClient

user_id = None

@pytest.mark.asyncio
async def test_create_user():
    global user_id
    unique_email = f"testuser_{uuid.uuid4().hex}@example.com"
    unique_username = f"testuser_{uuid.uuid4().hex}"
    async with AsyncClient(base_url="http://localhost:8000") as ac:
        user_data = {"username": unique_username, "email": unique_email, "password": "password123"}
        response = await ac.post("/users/", json=user_data)

    print(response.status_code, response.text)  # Debug
    assert response.status_code == 200

    data = response.json()
    user_id = data["id"]

@pytest.mark.asyncio
async def test_read_user():
    global user_id
    assert user_id is not None, "User ID is not set. Ensure test_create_user runs first."

    async with AsyncClient(base_url="http://localhost:8000") as ac:
        response = await ac.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert "username" in data
    assert "email" in data

@pytest.mark.asyncio
async def test_read_users():
    async with AsyncClient(base_url="http://localhost:8000") as ac:
        response = await ac.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

@pytest.mark.asyncio
async def test_update_user():
    global user_id
    assert user_id is not None, "User ID is not set. Ensure test_create_user runs first."

    async with AsyncClient(base_url="http://localhost:8000") as ac:
        user_update_data = {"username": "updateduser", "email": "updateduser@example.com"}
        response = await ac.put(f"/users/{user_id}", json=user_update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == user_update_data["username"]
    assert data["email"] == user_update_data["email"]

@pytest.mark.asyncio
async def test_delete_user():
    global user_id
    assert user_id is not None, "User ID is not set. Ensure test_create_user runs first."

    async with AsyncClient(base_url="http://localhost:8000") as ac:
        response = await ac.delete(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert "username" in data
    assert "email" in data
