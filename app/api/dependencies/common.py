"""Module containing common dependencies."""

from app.clients import IpstackClient
from typing import Callable, Type, TypeVar
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.base import SQLAlchemyRepository
from app.api.dependencies.database import get_async_session

SQLA_REPO_TYPE = TypeVar("SQLA_REPO_TYPE", bound=SQLAlchemyRepository)


def get_repository_dependency(
    repo_type: Type[SQLA_REPO_TYPE],
) -> Callable[[AsyncSession], Type[SQLA_REPO_TYPE]]:
    """Returns specified repository seeded with an async database session."""

    def get_repo(
        db: AsyncSession = Depends(get_async_session),
    ) -> Type[SQLA_REPO_TYPE]:
        return repo_type(db=db)

    return get_repo


def ipstack_client_dependency() -> IpstackClient:
    """Ipstack client dependency."""
    return IpstackClient()
