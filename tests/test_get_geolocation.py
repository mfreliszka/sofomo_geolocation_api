"""Module containing tests for the get_geolocation endpoint."""

from fastapi import FastAPI, status
import pytest

from syrupy.assertion import SnapshotAssertion


@pytest.mark.anyio
async def test_get_existing_geolocation(
    app: FastAPI,
    IPGeolocation1_InDB_Model: pytest.fixture,
    snapshot: SnapshotAssertion,
    valid_ip1: pytest.fixture,
    httpx_async_client: pytest.fixture,
):
    """Test retrieving an existing geolocation from the database."""
    response = await httpx_async_client.get(
        app.url_path_for("get_geolocation_from_database"),
        params={"ip_address": valid_ip1},
    )

    assert response.json() == snapshot, "Actual response did not match snapshot"
    assert response.status_code == status.HTTP_200_OK, (
        f"Response status code: {response.status_code}"
    )
    assert response.headers["Content-Type"] == "application/json", (
        f"Response content type: {response.headers['Content-Type']}"
    )


@pytest.mark.anyio
async def test_get_not_existing_geolocation(
    app: FastAPI,
    snapshot: SnapshotAssertion,
    non_existent_ip: pytest.fixture,
    httpx_async_client: pytest.fixture,
):
    """Test retrieving not existing geolocation from the database."""
    response = await httpx_async_client.get(
        app.url_path_for("get_geolocation_from_database"),
        params={"ip_address": non_existent_ip},
    )

    assert response.json() == snapshot, "Actual response did not match snapshot"
    assert response.status_code == status.HTTP_404_NOT_FOUND, (
        f"Response status code: {response.status_code}"
    )
    assert response.headers["Content-Type"] == "application/json", (
        f"Response content type: {response.headers['Content-Type']}"
    )


@pytest.mark.anyio
async def test_get_invalid_ip_address(
    app: FastAPI,
    snapshot: SnapshotAssertion,
    invalid_ip: pytest.fixture,
    httpx_async_client: pytest.fixture,
):
    """Test retrieving invalid IP address from the database."""
    response = await httpx_async_client.get(
        app.url_path_for("get_geolocation_from_database"),
        params={"ip_address": invalid_ip},
    )

    assert response.json() == snapshot, "Actual response did not match snapshot"
    assert response.status_code == status.HTTP_400_BAD_REQUEST, (
        f"Response status code: {response.status_code}"
    )
    assert response.headers["Content-Type"] == "application/json", (
        f"Response content type: {response.headers['Content-Type']}"
    )
