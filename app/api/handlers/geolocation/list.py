"""Module containing list geolocation data endpoint."""

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from app.api.dependencies.common import get_repository_dependency
from app.db.repositories.geolocation import IPGeolocationRepository
from app.models.models import IPGeolocationInDB

router = APIRouter()


@router.get(
    "/list",
    # response_model=List[IPGeolocationInDB],
    name="list_geolocations",
    status_code=status.HTTP_200_OK,
)
async def list_geolocations(
    ip_geolocation_repo: IPGeolocationRepository = Depends(
        get_repository_dependency(IPGeolocationRepository)
    ),
) -> JSONResponse:
    """Get all geolocations from database."""
    records = await ip_geolocation_repo.list()

    return [IPGeolocationInDB.model_validate(record) for record in records]
