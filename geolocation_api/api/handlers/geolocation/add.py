"""Module containing add geolocation data endpoint."""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from geolocation_api.clients import IpstackClient
from geolocation_api.api.dependencies.common import ipstack_client_dependency

router = APIRouter()


@router.get("/add")
async def add_geolocation(
    ip_address: str,
    ipstack_client: IpstackClient = Depends(ipstack_client_dependency),
) -> JSONResponse:
    """Add geolocation to database."""
    try:
        async with ipstack_client as client:
            geolocation_response = await client.get_geolocation(ip_address)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return JSONResponse(content=geolocation_response, status_code=201)
