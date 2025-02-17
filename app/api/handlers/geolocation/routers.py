"""Module containing geolocation api router configuration."""

from fastapi import APIRouter
from app.api.handlers.geolocation.add import (
    router as add_geolocation_router,
)
from app.api.handlers.geolocation.get import (
    router as get_geolocation_router,
)
from app.api.handlers.geolocation.delete import (
    router as delete_geolocation_router,
)
from app.api.handlers.geolocation.list import (
    router as list_geolocation_router,
)


def geolocation_api_router_factory() -> APIRouter:
    """Construct geolocation api router."""
    geolocation_prefix = "/geolocation"

    router = APIRouter(prefix=geolocation_prefix)

    endpoint_routers = [
        add_geolocation_router,
        get_geolocation_router,
        delete_geolocation_router,
        list_geolocation_router,
    ]

    for endpoint_router in endpoint_routers:
        router.include_router(endpoint_router)

    return router
