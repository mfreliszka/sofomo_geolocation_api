"""Test configuration and fixtures."""
import json
from typing import AsyncGenerator, Generator
import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool
from unittest.mock import AsyncMock

from app.db.repositories.geolocation import IPGeolocationRepository
from app.models.models import IPGeolocationInDB

from app.db.models.base import Base
from app.main import application_factory
from app.api.dependencies.common import get_repository_dependency, ipstack_client_dependency
from app.db.repositories.geolocation import IPGeolocationRepository
from app.clients import IpstackClient
from pathlib import Path
from sqlalchemy.orm import sessionmaker


@pytest.fixture
def app() -> FastAPI:
    """Get fastapi application instance."""
    return application_factory()

# @pytest.fixture
# def mock_async_engine():
#     """Create a mock async engine for testing."""
#     engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
#     return engine

@pytest.fixture
def mock_async_engine():
    """Create a mock async engine for testing."""
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=True
    )
    return engine



@pytest.fixture
async def mock_db_session(mock_async_engine):
    """Return a mocked database session."""
    async_session = sessionmaker(
        bind=mock_async_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with async_session() as session:
        yield session

@pytest.fixture(autouse=True)
def override_db_engine(monkeypatch, mock_async_engine):
    """Override the get_async_engine function to return a mock engine."""
    monkeypatch.setattr("app.db.db_session.get_async_engine", lambda: mock_async_engine)


@pytest.fixture
def mock_ip_geolocation_repo(mock_db_session):
    """Mock the IPGeolocationRepository using a mocked AsyncSession."""
    repo = IPGeolocationRepository(mock_db_session)

    # Mock get_by_ip to return None (simulate no existing record)
    repo.get_by_ip = AsyncMock(return_value=None)

    # Mock create method
    async def create_mock(obj_new):
        """Simulate inserting into the database."""
        return IPGeolocationInDB(id=1, **obj_new.model_dump())

    repo.create = AsyncMock(side_effect=create_mock)

    return repo


@pytest.fixture
def mock_ipstack_client():
    """Mock the IpstackClient dependency while preserving async context manager behavior."""
    
    class MockIpstackClient:
        """Mocked version of IpstackClient."""
        
        def __init__(self):
            # Load mock response from a file
            json_path = Path(__file__).parent / "json/response.json"
            with json_path.open("r", encoding="utf-8") as file:
                self.mock_response = json.load(file)

        async def __aenter__(self):
            """Simulate entering the async context."""
            return self  # Return itself as a context manager

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            """Simulate exiting the async context."""
            pass  # No cleanup needed

        async def get_geolocation(self, ip_address: str):
            """Mocked get_geolocation method."""
            return self.mock_response

    return MockIpstackClient()

# Helper fixtures dla często używanych operacji
@pytest.fixture
def valid_ip() -> str:
    """Return a valid IP address for testing."""
    return "8.8.8.8"

@pytest.fixture
def invalid_ip() -> str:
    """Return an invalid IP address for testing."""
    return "invalid_ip"

@pytest.fixture
def non_existent_ip() -> str:
    """Return a non-existent IP address for testing."""
    return "1.1.1.1"
