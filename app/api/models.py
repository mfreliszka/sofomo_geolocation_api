"""Module containing database models."""

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Geolocation(Base):
    __tablename__ = "geolocations"

    id = Column(Integer, primary_key=True, index=True)
    ip = Column(String, unique=True, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    city = Column(String, nullable=True)
    country = Column(String, nullable=True)
