"""Domain Repository for 'Geolocation' entity.

All logic related to the geolocation entity is defined and grouped here.
"""

from app.db.models.models import IPGeolocation
from app.db.repositories.base import SQLAlchemyRepository
from app.models.models import IPGeolocationCreate


class IPGeolocationRepository(SQLAlchemyRepository):
    """Handle all logic related to IPGeolocation entity.

    Inheritence from 'SQLAlchemyRepository' allows for
    crud functionality, only schema and models used have to be defined.
    """

    sqla_model = IPGeolocation

    create_schema = IPGeolocationCreate
