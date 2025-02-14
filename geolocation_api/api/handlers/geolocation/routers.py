"""Module containing geolocation api router configuration."""

from fastapi import APIRouter
from geolocation_api.api.handlers.geolocation.add import (
    router as add_geolocation_router,
)


def geolocation_api_router_factory() -> APIRouter:
    """Construct geolocation api router."""
    geolocation_prefix = "/geolocation"

    router = APIRouter(prefix=geolocation_prefix)

    endpoint_routers = [
        add_geolocation_router,
    ]

    for endpoint_router in endpoint_routers:
        router.include_router(endpoint_router)

    return router
