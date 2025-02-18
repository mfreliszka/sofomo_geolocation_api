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

    async def list(self, offset: int = 0, limit: int = 10):
        """Get paginated list of IP geolocations."""
        query = """
            SELECT *
            FROM ip_geolocation
            ORDER BY id
            LIMIT :limit OFFSET :offset
        """
        records = await self.db.fetch_all(
            query=query,
            values={"limit": limit, "offset": offset}
        )
        return records
