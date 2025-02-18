"""Module containing client classes."""

import httpx
from config.settings import settings
from app.decorators import handle_ipstack_errors
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from json import JSONDecodeError
from loguru import logger

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

        try:
            response = await self.client.get(
                f"{self.base_url}/{ip_address}?access_key={self.api_key}",
                timeout=settings.ipstack_timeout,
            )

            response.raise_for_status()
            return response.json()
        except httpx.TimeoutException as timeout_exc:
            logger.error(f"IPStack API request timed out.")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Request timed out. Please try again later."
            )
        except httpx.HTTPStatusError as status_exc:
            logger.error(f"IPStack API returned error status: {status_exc.response.status_code}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Geolocation service is temporarily unavailable. Please try again later."
            )
        except Exception as e:
            logger.error(f"Unexpected error in IPStack API request: {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Unexpected error in IPStack API request: {e}"
            )
