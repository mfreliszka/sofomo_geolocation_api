"""Module containing common dependencies."""

from functools import lru_cache
from app.clients import IpstackClient


@lru_cache
def ipstack_client_dependency() -> IpstackClient:
    """Ipstack client dependency."""
    return IpstackClient()
