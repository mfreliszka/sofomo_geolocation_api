"""Module containing domain repository for Geolocation entity."""

from app.db.models.models import IPGeolocation
from app.db.repositories.base import SQLAlchemyRepository
from app.models.models import IPGeolocationCreate
from sqlalchemy import select, func


class IPGeolocationRepository(SQLAlchemyRepository):
    """Handle all logic related to IPGeolocation entity.

    Inheritence from 'SQLAlchemyRepository' allows for
    crud functionality, only schema and models used have to be defined.
    """

    sqla_model = IPGeolocation

    create_schema = IPGeolocationCreate

    async def count(self) -> int:
        """Get total count of records."""
        query = select(func.count()).select_from(self.sqla_model)
        result = await self.db.execute(query)
        return result.scalar()

    async def list(self, offset: int = 0, limit: int = 10):
        """Get paginated list of IP geolocations."""
        query = (
            select(self.sqla_model)
            .order_by(self.sqla_model.id)
            .offset(offset)
            .limit(limit)
        )
        result = await self.db.execute(query)
        return result.scalars().all()
