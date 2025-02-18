"""Middleware for the application."""

from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from loguru import logger
import httpx
from app.clients import IpstackClient
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from app.db.db_session import get_async_engine
from asyncpg.exceptions import ConnectionDoesNotExistError
from sqlalchemy.exc import OperationalError

class DatabaseAvailabilityMiddleware(BaseHTTPMiddleware):
    """Middleware to check database availability."""
    
    async def dispatch(self, request: Request, call_next):
        """Check database availability before processing the request."""
        try:
            engine = get_async_engine()
            async with engine.connect() as connection:
                await connection.execute(text("SELECT 1"))
                await connection.commit()
        except (SQLAlchemyError, ConnectionDoesNotExistError, OperationalError) as e:
            logger.error(f"Database health check failed: {str(e)}")
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content={
                    "detail": "Database service is temporarily unavailable. Please try again later."
                }
            )
        except Exception as e:
            logger.error(f"Unexpected database error: {str(e)}")
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content={
                    "detail": "Database service is temporarily unavailable. Please try again later."
                }
            )

        response = await call_next(request)
        return response