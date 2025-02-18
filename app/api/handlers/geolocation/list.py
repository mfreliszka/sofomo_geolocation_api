"""Module containing list geolocation data endpoint."""

from fastapi import APIRouter, Depends, status, Query
from fastapi.responses import JSONResponse
from typing import Optional
from app.api.dependencies.common import get_repository_dependency
from app.db.repositories.geolocation import IPGeolocationRepository
from app.models.models import IPGeolocationInDB
from pydantic import BaseModel

router = APIRouter()


class PaginatedResponse(BaseModel):
    items: list[IPGeolocationInDB]
    total: int
    offset: int
    limit: int


@router.get(
    "/geolocation/list",
    response_model=PaginatedResponse,
    name="list_all_geolocations_from_database",
    status_code=status.HTTP_200_OK,
)
async def list_geolocations(
    offset: Optional[int] = Query(default=0, ge=0, description="Skip N records"),
    limit: Optional[int] = Query(default=10, ge=1, le=100, description="Limit the number of records returned"),
    ip_geolocation_repo: IPGeolocationRepository = Depends(
        get_repository_dependency(IPGeolocationRepository)
    ),
) -> JSONResponse:
    """Get all geolocations from database."""
    records = await ip_geolocation_repo.list(offset=offset, limit=limit)
    total = await ip_geolocation_repo.count()

    return PaginatedResponse(
        items=[IPGeolocationInDB.model_validate(record) for record in records],
        total=total,
        offset=offset,
        limit=limit
    )
