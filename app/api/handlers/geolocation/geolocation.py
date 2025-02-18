"""Module containing geolocation data endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.clients import IpstackClient
from loguru import logger
from app.api.dependencies.common import get_repository_dependency
from app.db.repositories.geolocation import IPGeolocationRepository
from app.models.models import IPGeolocationInDB
from app.api.dependencies.common import (
    ipstack_client_dependency,
    get_repository_dependency,
)
from app.models.models import IPGeolocationCreate, IPGeolocationInDB
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError
router = APIRouter()


@router.get(
    "/geolocation",
    response_model=IPGeolocationInDB,
    name="get_geolocation_from_database",
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

class IPAddressRequest(BaseModel):
    """Request model for add geolocation endpoint."""

    ip_address: str


@router.post(
    "/geolocation",
    response_model=IPGeolocationInDB,
    name="add_geolocation_to_database",
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
            print(geolocation_response)
    except HTTPException as http_exc:
        raise
    # except Exception as e:
    #     logger.error(f"Unexpected error in add_geolocation: {str(e)}")
    #     raise HTTPException(status_code=500, detail=str(e))

    ip_geolocation_new = IPGeolocationCreate(**geolocation_response)
    created_record = await ip_geolocation_repo.create(obj_new=ip_geolocation_new)

    return created_record
    # try:
    #     # First try to get existing record
    #     try:
    #         existing_record = await ip_geolocation_repo.get_by_ip(request.ip_address)
    #         if existing_record:
    #             return JSONResponse(
    #                 status_code=status.HTTP_200_OK,
    #                 content={
    #                     "message": f"Geolocation for IP {request.ip_address} already exists in database",
    #                     "data": jsonable_encoder(
    #                         IPGeolocationInDB.model_validate(existing_record)
    #                     ),
    #                 },
    #             )
    #     except SQLAlchemyError as db_error:
    #         logger.error(f"Database error while checking existing record: {str(db_error)}")
    #         raise HTTPException(
    #             status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
    #             detail="Database service is temporarily unavailable. Please try again later."
    #         )

    #     # Try to get data from IPStack
    #     try:
    #         async with ipstack_client as client:
    #             geolocation_response = await client.get_geolocation(request.ip_address)
    #     except HTTPException:
    #         # Re-raise HTTP exceptions from IPStack client
    #         raise
    #     except Exception as e:
    #         logger.error(f"Unexpected error while fetching geolocation: {str(e)}")
    #         raise HTTPException(
    #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #             detail="An unexpected error occurred while processing your request."
    #         )

    #     # Try to create new record
    #     try:
    #         ip_geolocation_new = IPGeolocationCreate(**geolocation_response)
    #         created_record = await ip_geolocation_repo.create(obj_new=ip_geolocation_new)
    #         return created_record
    #     except SQLAlchemyError as db_error:
    #         logger.error(f"Database error while creating new record: {str(db_error)}")
    #         raise HTTPException(
    #             status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
    #             detail="Database service is temporarily unavailable. Please try again later."
    #         )
    #     except ValidationError as val_error:
    #         logger.error(f"Validation error with IPStack response: {str(val_error)}")
    #         raise HTTPException(
    #             status_code=status.HTTP_502_BAD_GATEWAY,
    #             detail="Received invalid data format from geolocation service."
    #         )

    # except HTTPException:
    #     raise
    # except Exception as e:
    #     logger.error(f"Unexpected error in add_geolocation: {str(e)}")
    #     raise HTTPException(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         detail="An unexpected error occurred while processing your request."
    #     )


@router.delete(
    "/geolocation",
    name="delete_geolocation_from_database",
    status_code=status.HTTP_200_OK,
)
async def delete_geolocation(
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
