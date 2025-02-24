"""Module contains fastapi application configuration & application factory."""

from config.settings import settings
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.router import api_router_factory
from app.middleware import DatabaseAvailabilityMiddleware
from app.db.db_session import sessionmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Function that handles startup and shutdown events.
    To understand more, read https://fastapi.tiangolo.com/advanced/events/
    """
    yield
    if sessionmanager._engine is not None:
        # Close the DB connection
        await sessionmanager.close()


def application_factory() -> FastAPI:
    """
    Configure fastapi application.
    """
    api_url_prefix = "/api"

    app = FastAPI(
        lifespan=lifespan,
        title=settings.project_name,
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        servers=[
            {"url": settings.application_url},
        ],
    )

    if not settings.TESTING:
        app.add_middleware(DatabaseAvailabilityMiddleware)
    app.include_router(api_router_factory(api_url_prefix))

    return app
