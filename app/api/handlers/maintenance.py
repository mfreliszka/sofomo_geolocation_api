"""Module containing maintenance endpoints."""

from time import time

from fastapi import APIRouter

from pydantic import BaseModel

router = APIRouter()


class Pong(BaseModel):
    """Model containig simple pong response."""

    message: str
    timestamp: float


@router.get("/ping", name="ping", response_model=Pong)
async def ping() -> Pong:
    """Return ok simply when server is available."""
    return Pong(message="pong", timestamp=time())
