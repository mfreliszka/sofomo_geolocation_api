"""Module containing tests for the get_geolocation endpoint."""

import json
from fastapi import status
import pytest

from syrupy.assertion import SnapshotAssertion


@pytest.mark.anyio
async def test_add_new_geolocation(
    app: pytest.fixture,
    snapshot: SnapshotAssertion,
    valid_ip1: pytest.fixture,
    httpx_async_client: pytest.fixture,
):
    """Test adding a new geolocation to the database."""
    response = await httpx_async_client.post(
        app.url_path_for("add_geolocation_to_database"),
        content=json.dumps(dict({"ip_address": valid_ip1})),
        headers={"Content-Type": "application/json"},
    )

    assert response.json() == snapshot, "Actual response did not match snapshot"
    assert response.status_code == status.HTTP_201_CREATED, (
        f"Response status code: {response.status_code}"
    )
    assert response.headers["Content-Type"] == "application/json", (
        f"Response content type: {response.headers['Content-Type']}"
    )


@pytest.mark.anyio
async def test_add_existing_geolocation(
    app: pytest.fixture,
    IPGeolocation1_InDB_Model: pytest.fixture,
    snapshot: SnapshotAssertion,
    valid_ip1: pytest.fixture,
    httpx_async_client: pytest.fixture,
):
    """Test adding an existing geolocation to the database."""
    response = await httpx_async_client.post(
        app.url_path_for("add_geolocation_to_database"),
        content=json.dumps(dict({"ip_address": valid_ip1})),
        headers={"Content-Type": "application/json"},
    )

    assert response.json() == snapshot, "Actual response did not match snapshot"
    assert response.status_code == status.HTTP_200_OK, (
        f"Response status code: {response.status_code}"
    )
    assert response.headers["Content-Type"] == "application/json", (
        f"Response content type: {response.headers['Content-Type']}"
    )


@pytest.mark.anyio
async def test_add_invalid_ip_address(
    app: pytest.fixture,
    snapshot: SnapshotAssertion,
    invalid_ip: pytest.fixture,
    httpx_async_client: pytest.fixture,
):
    """Test adding invalid IP address to the database."""
    response = await httpx_async_client.post(
        app.url_path_for("add_geolocation_to_database"),
        content=json.dumps(dict({"ip_address": invalid_ip})),
        headers={"Content-Type": "application/json"},
    )

    assert response.json() == snapshot, "Actual response did not match snapshot"
    assert response.status_code == status.HTTP_400_BAD_REQUEST, (
        f"Response status code: {response.status_code}"
    )
    assert response.headers["Content-Type"] == "application/json", (
        f"Response content type: {response.headers['Content-Type']}"
    )
