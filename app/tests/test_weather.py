import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_get_weather():
    async with AsyncClient(base_url="http://localhost:8000") as ac:
        response = await ac.get("/weather", params={"city": "Paris", "hourly": "temperature_2m", "daily": "temperature_2m_max", "timezone": "auto"})
    assert response.status_code == 200
    data = response.json()
    assert "latitude" in data
    assert "longitude" in data
    assert "hourly" in data
    assert "daily" in data

@pytest.mark.asyncio
async def test_get_current_weather():
    async with AsyncClient(base_url="http://localhost:8000") as ac:
        response = await ac.get("/current_weather", params={"city": "Paris", "timezone": "auto"})
    assert response.status_code == 200
    data = response.json()
    assert "temperature" in data
    assert "time" in data
    assert "is_day" in data
    assert "interval" in data