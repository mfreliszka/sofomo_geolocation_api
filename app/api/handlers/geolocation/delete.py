"""Module containing get geolocation data endpoint."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from loguru import logger
from app.api.dependencies.common import get_repository_dependency
from app.db.repositories.geolocation import IPGeolocationRepository
from app.models.models import IPGeolocationInDB

router = APIRouter()


@router.delete(
    "/delete",
    name="delete_geolocation",
    status_code=status.HTTP_200_OK,
)
async def get_geolocation(
    ip_address: str,
    ip_geolocation_repo: IPGeolocationRepository = Depends(
        get_repository_dependency(IPGeolocationRepository)
    ),
) -> IPGeolocationInDB:
    """Delete geolocation from database."""
    deleted_record = await ip_geolocation_repo.delete(ip_address)
    if not deleted_record:
        logger.warning(f"Geolocation for IP {ip_address} not found in database.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Geolocation for IP {ip_address} not found in database.",
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": f"Geolocation for IP {ip_address} deleted from database.",
            "data": jsonable_encoder(IPGeolocationInDB.model_validate(deleted_record)),
        },
    )
