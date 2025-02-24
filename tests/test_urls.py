"""Module containig tests for endpoint urls."""

import pytest
from fastapi import FastAPI


@pytest.mark.asyncio
async def test_get_geolocation_url(app: FastAPI):
    url = app.url_path_for("get_geolocation_from_database")
    assert url == "/api/geolocation"


@pytest.mark.asyncio
async def test_add_geolocation_url(app: FastAPI):
    url = app.url_path_for("add_geolocation_to_database")
    assert url == "/api/geolocation"


@pytest.mark.asyncio
async def test_delete_geolocation_url(app: FastAPI):
    url = app.url_path_for("delete_geolocation_from_database")
    assert url == "/api/geolocation"


@pytest.mark.asyncio
async def test_list_geolocations_url(app: FastAPI):
    url = app.url_path_for("list_all_geolocations_from_database")
    assert url == "/api/geolocation/list"
