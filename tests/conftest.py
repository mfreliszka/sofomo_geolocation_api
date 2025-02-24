"""Module containing common fixtures for testing."""

import json
import pytest
import pytest_asyncio

from fastapi import FastAPI
from app.api.dependencies.common import ipstack_client_dependency
from app.main import application_factory
from datetime import datetime
from httpx import AsyncClient, ASGITransport
from pathlib import Path

from fastapi.testclient import TestClient
from app.db.db_session import get_db_session
from app.db.models.base import Base
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker

from app.db.models.models import IPGeolocation as IPGeolocationModel
from app.models.models import IPGeolocationInDB


# Test database URL (SQLite in-memory for fast tests)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create test engine and session factory
test_engine = create_async_engine(TEST_DATABASE_URL, echo=True)
TestSessionLocal = sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False
)


@pytest.fixture
def app() -> FastAPI:
    """Get fastapi application instance."""
    return application_factory()


@pytest.fixture
def client(app):
    with TestClient(app) as c:
        yield c


@pytest_asyncio.fixture
async def httpx_async_client(app: FastAPI):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture(scope="function")
async def db_session() -> AsyncSession:
    """Creates a new test database session for each test."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  # Create tables

    async with TestSessionLocal() as test_session:
        # Mock the database updated_at field from BaseDBModel so it always has the same timestamp in tests.
        original_add = test_session.add

        def add_and_override(instance):
            if hasattr(instance, "updated_at"):
                instance.updated_at = datetime(2020, 1, 1)
            original_add(instance)

        test_session.add = add_and_override

        yield test_session  # Provide session to test
        await test_session.rollback()  # Rollback changes after test

    # Drop all tables after test session ends
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function", autouse=True)
async def session_override(app, db_session):
    async def get_db_session_override():
        yield db_session

    app.dependency_overrides[get_db_session] = get_db_session_override


@pytest.fixture
def valid_ip1() -> str:
    """Return a valid IP address for testing."""
    return "8.8.8.8"


@pytest.fixture
def valid_ip2() -> str:
    """Return a valid IP address for testing."""
    return "8.8.8.7"


@pytest.fixture
def invalid_ip() -> str:
    """Return an invalid IP address for testing."""
    return "invalid_ip"


@pytest.fixture
def non_existent_ip() -> str:
    """Return a non-existent IP address for testing."""
    return "1.1.1.1"


@pytest.fixture
def IPGeolocation1_InDB_Schema(valid_ip1: str) -> IPGeolocationInDB:
    """Returns a json compatible dict of example ParentInDB model"""
    return IPGeolocationInDB(
        id=1,
        ip=valid_ip1,
        type="IPv4",
        continent_code="NA",
        continent_name="North America",
        country_code="US",
        country_name="United States",
        region_code="CA",
        region_name="California",
        city="Mountain View",
        zip="94043",
        latitude=37.422,
        longitude=-122.084,
        updated_at=datetime(2025, 2, 20, 12, 0, 0).isoformat(),
    )


@pytest.fixture
async def IPGeolocation1_InDB_Model(
    db_session: AsyncSession,
    IPGeolocation1_InDB_Schema: pytest.fixture,
) -> IPGeolocationModel:
    geolocation = IPGeolocationModel(**IPGeolocation1_InDB_Schema.model_dump())

    db_session.add(geolocation)
    await db_session.commit()
    await db_session.refresh(geolocation)


@pytest.fixture
def IPGeolocation2_InDB_Schema(valid_ip2: str) -> IPGeolocationInDB:
    """Returns a json compatible dict of example ParentInDB model"""
    return IPGeolocationInDB(
        id=2,
        ip=valid_ip2,
        type="IPv4",
        continent_code="NA",
        continent_name="North America",
        country_code="US",
        country_name="United States",
        region_code="OH",
        region_name="Ohio",
        city="Mountain View",
        zip="94043",
        latitude=37.422,
        longitude=-122.084,
        updated_at=datetime(2025, 2, 20, 12, 0, 0).isoformat(),
    )


@pytest.fixture
async def IPGeolocation2_InDB_Model(
    db_session: AsyncSession,
    IPGeolocation2_InDB_Schema: pytest.fixture,
) -> IPGeolocationModel:
    geolocation = IPGeolocationModel(**IPGeolocation2_InDB_Schema.model_dump())

    db_session.add(geolocation)
    await db_session.commit()
    await db_session.refresh(geolocation)


class MockIpstackClient:
    def __init__(self):
        with Path("tests/json/ipstack_geolocation_response.json").open(
            encoding="utf-8"
        ) as json_file:
            self.ipstack_geolocation_response = json.load(json_file)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    async def get_geolocation(self, ip_address: str):
        return self.ipstack_geolocation_response


@pytest.fixture(scope="function", autouse=True)
def mock_ipstack_client_dependency(app):
    """Mock FastAPI dependency for IpstackClient to prevent real API calls."""

    async def _mock_ipstack_client():
        return MockIpstackClient()

    app.dependency_overrides[ipstack_client_dependency] = _mock_ipstack_client

    yield

    app.dependency_overrides.clear()
