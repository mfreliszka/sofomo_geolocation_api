"""Module containing client classes."""

import httpx
from config.settings import settings
from app.decorators import handle_ipstack_errors


class IpstackClient:
    """Client for IPStack api."""

    def __init__(self) -> None:
        self.api_key = settings.ipstack_access_key
        self.base_url = settings.ipstack_api_url
        self.client = None

    async def __aenter__(self):
        """Asynchronous enter context."""
        self.client = httpx.AsyncClient()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Asynchronous exit context."""
        if self.client:
            await self.client.aclose()

    @handle_ipstack_errors
    async def get_geolocation(self, ip_address: str) -> httpx.Response:
        """Get geolocation for given ip address."""
        if not self.client:
            raise RuntimeError("Client must be used within context manager")

        response = await self.client.get(
            f"{self.base_url}/{ip_address}?access_key={self.api_key}",
            timeout=settings.ipstack_timeout,
        )

        return response.json()
