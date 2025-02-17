"""Module containing get geolocation data endpoint."""

from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger
from app.api.dependencies.common import get_repository_dependency
from app.db.repositories.geolocation import IPGeolocationRepository
from app.models.models import IPGeolocationInDB

router = APIRouter()


@router.get(
    "/get",
    response_model=IPGeolocationInDB,
    name="get_geolocation",
    status_code=status.HTTP_200_OK,
)
async def get_geolocation(
    ip_address: str, # https://www.rfc-editor.org/rfc/rfc2616#section-9.3
    ip_geolocation_repo: IPGeolocationRepository = Depends(
        get_repository_dependency(IPGeolocationRepository)
    ),
) -> IPGeolocationInDB:
    """Get geolocation from database."""
    existing_record = await ip_geolocation_repo.get_by_ip(ip_address)
    if not existing_record:
        logger.warning(f"Geolocation for IP {ip_address} not found in database.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Geolocation for IP {ip_address} not found in database.",
        )

    return existing_record
