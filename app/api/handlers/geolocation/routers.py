"""Module containing geolocation api router configuration."""

from fastapi import APIRouter
from app.api.handlers.geolocation.geolocation import (
    router as add_get_delete_geolocation_router,
)
from app.api.handlers.geolocation.list import (
    router as list_geolocation_router,
)


def geolocation_api_router_factory() -> APIRouter:
    """Construct geolocation api router."""
    router = APIRouter()

    endpoint_routers = [
        add_get_delete_geolocation_router,
        list_geolocation_router,
    ]

    for endpoint_router in endpoint_routers:
        router.include_router(endpoint_router)

    return router
