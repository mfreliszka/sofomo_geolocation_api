"""Module contains fastapi application configuration & application factory."""

from config.settings import Settings
from fastapi import FastAPI
from geolocation_api.router import api_router_factory


def application_factory() -> FastAPI:
    """
    Configure fastapi application.
    """
    settings = Settings()

    api_url_prefix = "/api"

    app = FastAPI(
        title="Sofomo Geolocation API",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        servers=[
            {"url": settings.application_url},
        ],
    )

    app.include_router(api_router_factory(api_url_prefix))

    return app
