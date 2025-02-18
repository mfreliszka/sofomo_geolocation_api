"""Test configuration and fixtures."""
import asyncio
from typing import AsyncGenerator, Generator
import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

from app.db.models.base import Base
from app.main import application_factory
from app.api.dependencies.common import get_repository_dependency, ipstack_client_dependency
from app.db.repositories.geolocation import IPGeolocationRepository
from app.clients import IpstackClient

# Test database URL - użyj zmiennych środowiskowych w prawdziwej aplikacji
TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/test_db"

# Mock data dla IpstackClient
MOCK_IPSTACK_RESPONSE = {
    "ip": "8.8.8.8",
    "type": "ipv4",
    "continent_code": "NA",
    "continent_name": "North America",
    "country_code": "US",
    "country_name": "United States",
    "region_code": "OH",
    "region_name": "Ohio",
    "city": "Glenmont",
    "zip": "44628",
    "latitude": 40.5369987487793,
    "longitude": -82.12859344482422
}

@pytest.fixture
def app() -> FastAPI:
    """Get fastapi application instance."""
    return application_factory()

@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an event loop for testing."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def test_db_engine():
    """Create a test database engine."""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        poolclass=NullPool,
    )
    
    # Utwórz wszystkie tabele
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    # Cleanup po testach
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest.fixture
async def test_db_session(test_db_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create a test database session."""
    async_session = async_sessionmaker(
        test_db_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    
    async with async_session() as session:
        yield session
        # Rollback po każdym teście
        await session.rollback()

@pytest.fixture
async def mock_ipstack_client() -> IpstackClient:
    """Create a mock IpstackClient."""
    class MockIpstackClient:
        async def __aenter__(self):
            return self
            
        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass
            
        async def get_geolocation(self, ip_address: str) -> dict:
            if ip_address == "invalid_ip":
                raise ValueError("Invalid IP address")
            return MOCK_IPSTACK_RESPONSE

    return MockIpstackClient()

@pytest.fixture
def override_dependencies(test_db_session, mock_ipstack_client,app: FastAPI) -> FastAPI:
    """Override dependencies for testing."""
    async def get_test_session():
        yield test_db_session

    async def get_test_ipstack_client():
        yield mock_ipstack_client

    app.dependency_overrides[get_repository_dependency(IPGeolocationRepository)] = get_test_session
    app.dependency_overrides[ipstack_client_dependency] = get_test_ipstack_client
    
    return app

@pytest.fixture
async def test_client(override_dependencies) -> AsyncGenerator[AsyncClient, None]:
    """Create a test client with overridden dependencies."""
    async with AsyncClient(app=override_dependencies, base_url="http://test") as client:
        yield client

@pytest.fixture
async def test_geolocation_in_db(test_db_session) -> dict:
    """Create a test geolocation record in the database."""
    from app.db.models.models import IPGeolocation
    
    geolocation = IPGeolocation(**MOCK_IPSTACK_RESPONSE)
    test_db_session.add(geolocation)
    await test_db_session.commit()
    await test_db_session.refresh(geolocation)
    
    return MOCK_IPSTACK_RESPONSE

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
