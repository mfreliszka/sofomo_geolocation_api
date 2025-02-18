import pytest
from fastapi import status, FastAPI
from httpx import AsyncClient, ASGITransport


@pytest.mark.asyncio
async def test_add_geolocation_to_db(mock_ipstack_client, mock_ip_geolocation_repo, app: FastAPI):
    """Test if geolocation data is correctly added to the database."""

    # Override dependencies
    app.dependency_overrides = {
        "ipstack_client_dependency": lambda: mock_ipstack_client,
        "get_repository_dependency(IPGeolocationRepository)": lambda: mock_ip_geolocation_repo,
    }

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
            response = await ac.post("/geolocation", json={"ip_address": "8.8.8.8"})

    # Assertions
    assert response.status_code == 201
    data = response.json()

    # Check that data is correctly inserted
    assert data["ip"] == "8.8.8.8"
    assert data["latitude"] == 37.386
    assert data["longitude"] == -122.084
    assert data["country_name"] == "United States"
    assert data["city"] == "Mountain View"

    # Verify the create method was called with expected data
    mock_ip_geolocation_repo.create.assert_called_once()

# @pytest.mark.asyncio
# async def test_add_geolocation(test_client: AsyncClient, valid_ip: str):
#     """Test adding new geolocation."""
#     response = await test_client.post(
#         "/geolocation",
#         json={"ip_address": valid_ip}
#     )
#     assert response.status_code == status.HTTP_201_CREATED
#     data = response.json()
#     assert data["ip"] == valid_ip

# @pytest.mark.asyncio
# async def test_get_geolocation(test_client, test_geolocation_in_db, valid_ip):
#     """Test getting existing geolocation."""
#     response = await test_client.get(f"/geolocation?ip_address={valid_ip}")
#     assert response.status_code == status.HTTP_200_OK
#     data = response.json()
#     assert data["ip"] == valid_ip

# @pytest.mark.asyncio
# async def test_delete_geolocation(test_client, test_geolocation_in_db, valid_ip):
#     """Test deleting existing geolocation."""
#     response = await test_client.delete(f"/geolocation?ip_address={valid_ip}")
#     assert response.status_code == status.HTTP_200_OK
#     data = response.json()
#     assert data["data"]["ip"] == valid_ip

# @pytest.mark.asyncio
# async def test_add_duplicate_geolocation(test_client, test_geolocation_in_db, valid_ip):
#     """Test adding duplicate geolocation."""
#     response = await test_client.post(
#         "/geolocation",
#         json={"ip_address": valid_ip}
#     )
#     assert response.status_code == status.HTTP_200_OK
#     assert "already exists" in response.json()["message"]

# @pytest.mark.asyncio
# async def test_get_non_existent_geolocation(test_client, non_existent_ip):
#     """Test getting non-existent geolocation."""
#     response = await test_client.get(f"/geolocation?ip_address={non_existent_ip}")
#     assert response.status_code == status.HTTP_404_NOT_FOUND

# @pytest.mark.asyncio
# async def test_delete_non_existent_geolocation(test_client, non_existent_ip):
#     """Test deleting non-existent geolocation."""
#     response = await test_client.delete(f"/geolocation?ip_address={non_existent_ip}")
#     assert response.status_code == status.HTTP_404_NOT_FOUND
