"""Contains fastapi router factory."""

from fastapi import APIRouter
from geolocation_api.api.handlers.maintenance import router as maintenance_router
from geolocation_api.api.handlers.geolocation.routers import (
    geolocation_api_router_factory,
)


def api_router_factory(url_prefix: str) -> APIRouter:
    """Construct main application router."""
    router = APIRouter(prefix=url_prefix)

    router.include_router(
        maintenance_router, prefix="/maintenance", tags=["Maintenance"]
    )
    router.include_router(geolocation_api_router_factory(), tags=["Geolocation"])

    return router
