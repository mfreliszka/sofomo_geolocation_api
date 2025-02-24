"""Module containing Sqlalchemy models."""

from sqlalchemy import Column, Numeric, String
# from sqlalchemy.orm import relationship

from app.db.models.base import Base, BaseDBModel
from app.db.models.metadata import metadata_family


class IPGeolocation(Base, BaseDBModel):
    """Database model representing IPGeolocation data."""

    __metadata__ = metadata_family

    ip = Column(String, index=True, unique=True)
    type = Column(String)
    continent_code = Column(String)
    continent_name = Column(String)
    country_code = Column(String)
    country_name = Column(String)
    region_code = Column(String)
    region_name = Column(String)
    city = Column(String)
    zip = Column(String)
    latitude = Column(Numeric(precision=16, scale=13))
    longitude = Column(Numeric(precision=16, scale=13))
