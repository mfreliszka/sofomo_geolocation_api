"""Module containing tests for the get_geolocation endpoint."""

from fastapi import status
import pytest

from syrupy.assertion import SnapshotAssertion


@pytest.mark.anyio
async def test_list_existing_geolocations(
    app: pytest.fixture,
    IPGeolocation1_InDB_Model: pytest.fixture,
    IPGeolocation2_InDB_Model: pytest.fixture,
    snapshot: SnapshotAssertion,
    httpx_async_client: pytest.fixture,
):
    """Test retrieving a list of existing geolocations from the database."""
    response = await httpx_async_client.get(
        app.url_path_for("list_all_geolocations_from_database"),
    )

    assert response.json() == snapshot, "Actual response did not match snapshot"
    assert response.status_code == status.HTTP_200_OK, (
        f"Response status code: {response.status_code}"
    )
    assert response.headers["Content-Type"] == "application/json", (
        f"Response content type: {response.headers['Content-Type']}"
    )


@pytest.mark.anyio
async def test_list_existing_geolocations_with_limit(
    app: pytest.fixture,
    IPGeolocation1_InDB_Model: pytest.fixture,
    IPGeolocation2_InDB_Model: pytest.fixture,
    snapshot: SnapshotAssertion,
    httpx_async_client: pytest.fixture,
):
    """Test retrieving a list of existing geolocations from the database with limit."""
    response = await httpx_async_client.get(
        app.url_path_for("list_all_geolocations_from_database"),
        params={"limit": 1},
    )

    assert response.json() == snapshot, "Actual response did not match snapshot"
    assert response.status_code == status.HTTP_200_OK, (
        f"Response status code: {response.status_code}"
    )
    assert response.headers["Content-Type"] == "application/json", (
        f"Response content type: {response.headers['Content-Type']}"
    )


@pytest.mark.anyio
async def test_list_existing_geolocations_with_limit_and_offset(
    app: pytest.fixture,
    IPGeolocation1_InDB_Model: pytest.fixture,
    IPGeolocation2_InDB_Model: pytest.fixture,
    snapshot: SnapshotAssertion,
    httpx_async_client: pytest.fixture,
):
    """Test retrieving a list of existing geolocations from the database with limit and offset."""
    response = await httpx_async_client.get(
        app.url_path_for("list_all_geolocations_from_database"),
        params={"limit": 1, "offset": 1},
    )

    assert response.json() == snapshot, "Actual response did not match snapshot"
    assert response.status_code == status.HTTP_200_OK, (
        f"Response status code: {response.status_code}"
    )
    assert response.headers["Content-Type"] == "application/json", (
        f"Response content type: {response.headers['Content-Type']}"
    )


@pytest.mark.anyio
async def test_empty_list_of_geolocations(
    app: pytest.fixture,
    snapshot: SnapshotAssertion,
    httpx_async_client: pytest.fixture,
):
    """Test retrieving a list of existing geolocations from the database."""
    response = await httpx_async_client.get(
        app.url_path_for("list_all_geolocations_from_database"),
    )

    assert response.json() == snapshot, "Actual response did not match snapshot"
    assert response.status_code == status.HTTP_200_OK, (
        f"Response status code: {response.status_code}"
    )
    assert response.headers["Content-Type"] == "application/json", (
        f"Response content type: {response.headers['Content-Type']}"
    )
