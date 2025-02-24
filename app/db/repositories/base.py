"""Abstract CRUD Repo definitions."""

from abc import ABC
from typing import TypeVar

from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.base import Base
from app.models.base import BaseSchema


SQLA_MODEL = TypeVar("SQLA_MODEL", bound=Base)
CREATE_SCHEMA = TypeVar("CREATE_SCHEMA", bound=BaseSchema)


class SQLAlchemyRepository(ABC):
    """Abstract SQLAlchemy repo defining basic database operations.

    Basic CRUD methods used by domain models to interact with the
    database are defined here.
    """

    def __init__(
        self,
        db: AsyncSession,
    ) -> None:
        self.db = db

    sqla_model = SQLA_MODEL

    create_schema = CREATE_SCHEMA

    async def create(self, obj_new: create_schema) -> sqla_model | None:
        """Commit new object to the database."""
        try:
            db_obj_new = self.sqla_model(**obj_new.model_dump())
            self.db.add(db_obj_new)

            await self.db.commit()
            await self.db.refresh(db_obj_new)

            logger.success(f"Created new entity: {db_obj_new}.")

            return db_obj_new

        except Exception as e:
            await self.db.rollback()

            logger.exception("Error while uploading new object to database")
            logger.exception(e)

            return None

    async def get_by_ip(
        self,
        ip: str,
    ) -> sqla_model | None:
        """Get object by ip or return None."""
        query = select(self.sqla_model).where(self.sqla_model.ip == ip)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def delete(
        self,
        ip: str,
    ) -> sqla_model | None:
        """Delete object from db by ip or None if object not found in db"""
        query = select(self.sqla_model).where(self.sqla_model.ip == ip)
        result = await self.db.execute(query)
        db_obj = result.scalar_one_or_none()

        if db_obj:
            await self.db.delete(db_obj)
            await self.db.commit()
            logger.success(f"Entity: {db_obj} successfully deleted from database.")
            return db_obj

        logger.warning(f"Object with ip = {ip} not found in database")
        return None
