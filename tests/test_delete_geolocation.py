"""Module containing tests for the get_geolocation endpoint."""

from fastapi import status
import pytest

from syrupy.assertion import SnapshotAssertion


@pytest.mark.anyio
async def test_delete_existing_geolocation(
    app: pytest.fixture,
    IPGeolocation1_InDB_Model: pytest.fixture,
    valid_ip1: pytest.fixture,
    httpx_async_client: pytest.fixture,
    mock_ipstack_client_dependency: pytest.fixture,
):
    """Test deleting an existing geolocation from the database."""
    response = await httpx_async_client.delete(
        app.url_path_for("delete_geolocation_from_database"),
        params={"ip_address": valid_ip1},
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT, (
        f"Response status code: {response.status_code}"
    )


@pytest.mark.anyio
async def test_delete_not_existing_geolocation(
    app: pytest.fixture,
    snapshot: SnapshotAssertion,
    non_existent_ip: pytest.fixture,
    httpx_async_client: pytest.fixture,
):
    """Test deleting not existing geolocation from the database."""
    response = await httpx_async_client.delete(
        app.url_path_for("delete_geolocation_from_database"),
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
async def test_delete_invalid_ip_address(
    app: pytest.fixture,
    snapshot: SnapshotAssertion,
    invalid_ip: pytest.fixture,
    httpx_async_client: pytest.fixture,
):
    """Test deleting invalid IP address from the database."""
    response = await httpx_async_client.delete(
        app.url_path_for("delete_geolocation_from_database"),
        params={"ip_address": invalid_ip},
    )

    assert response.json() == snapshot, "Actual response did not match snapshot"
    assert response.status_code == status.HTTP_400_BAD_REQUEST, (
        f"Response status code: {response.status_code}"
    )
    assert response.headers["Content-Type"] == "application/json", (
        f"Response content type: {response.headers['Content-Type']}"
    )
