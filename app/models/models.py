"""Pydantic models for IPGeolocation resource."""

import datetime as dt

from app.models.base import BaseSchema
from pydantic import ConfigDict


class IPGeolocationBase(BaseSchema):
    ip: str
    type: str | None
    continent_code: str | None
    continent_name: str | None
    country_code: str | None
    country_name: str | None
    region_code: str | None
    region_name: str | None
    city: str | None
    zip: str | None
    latitude: float
    longitude: float


class IPGeolocationCreate(IPGeolocationBase):
    pass


class IPGeolocationInDB(IPGeolocationBase):
    """Schema for 'IPGeolocation' in database."""

    id: int
    updated_at: dt.datetime

    model_config = ConfigDict(from_attributes=True)
