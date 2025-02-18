import pytest
from fastapi import status

@pytest.mark.asyncio
async def test_add_geolocation(test_client, valid_ip):
    """Test adding new geolocation."""
    response = await test_client.post(
        "/geolocation",
        json={"ip_address": valid_ip}
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["ip"] == valid_ip

@pytest.mark.asyncio
async def test_get_geolocation(test_client, test_geolocation_in_db, valid_ip):
    """Test getting existing geolocation."""
    response = await test_client.get(f"/geolocation?ip_address={valid_ip}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["ip"] == valid_ip

@pytest.mark.asyncio
async def test_delete_geolocation(test_client, test_geolocation_in_db, valid_ip):
    """Test deleting existing geolocation."""
    response = await test_client.delete(f"/geolocation?ip_address={valid_ip}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["data"]["ip"] == valid_ip

@pytest.mark.asyncio
async def test_add_duplicate_geolocation(test_client, test_geolocation_in_db, valid_ip):
    """Test adding duplicate geolocation."""
    response = await test_client.post(
        "/geolocation",
        json={"ip_address": valid_ip}
    )
    assert response.status_code == status.HTTP_200_OK
    assert "already exists" in response.json()["message"]

@pytest.mark.asyncio
async def test_get_non_existent_geolocation(test_client, non_existent_ip):
    """Test getting non-existent geolocation."""
    response = await test_client.get(f"/geolocation?ip_address={non_existent_ip}")
    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.asyncio
async def test_delete_non_existent_geolocation(test_client, non_existent_ip):
    """Test deleting non-existent geolocation."""
    response = await test_client.delete(f"/geolocation?ip_address={non_existent_ip}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
