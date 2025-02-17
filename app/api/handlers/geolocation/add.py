"""Module containing add geolocation data endpoint."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.clients import IpstackClient
from app.api.dependencies.common import (
    ipstack_client_dependency,
    get_repository_dependency,
)
from app.db.repositories.geolocation import IPGeolocationRepository
from app.models.models import IPGeolocationCreate, IPGeolocationInDB

router = APIRouter()


class IPAddressRequest(BaseModel):
    """Request model for add geolocation endpoint."""

    ip_address: str


@router.post(
    "/add",
    response_model=IPGeolocationInDB,
    name="add_geolocation",
    status_code=status.HTTP_201_CREATED,
)
async def add_geolocation(
    request: IPAddressRequest,
    ipstack_client: IpstackClient = Depends(ipstack_client_dependency),
    ip_geolocation_repo: IPGeolocationRepository = Depends(
        get_repository_dependency(IPGeolocationRepository)
    ),
) -> IPGeolocationInDB:
    """Add geolocation to database."""
    existing_record = await ip_geolocation_repo.get_by_ip(request.ip_address)
    if existing_record:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": f"Geolocation for IP {request.ip_address} already exists in database",
                "data": jsonable_encoder(
                    IPGeolocationInDB.model_validate(existing_record)
                ),
            },
        )

    try:
        async with ipstack_client as client:
            geolocation_response = await client.get_geolocation(request.ip_address)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    ip_geolocation_new = IPGeolocationCreate(**geolocation_response)
    created_record = await ip_geolocation_repo.create(obj_new=ip_geolocation_new)

    return created_record
