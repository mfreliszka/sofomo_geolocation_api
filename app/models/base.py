"""Base classes for pydantic domain models.

Allows for pydantic validation via inheritence from pydantics 'BaseModel'
"""

from pydantic import BaseModel


class BaseSchema(BaseModel):
    """Base pydantic schema for domain models.

    Share common logic here.
    """

    pass


class IDSchemaMixin(BaseModel):
    """Base pydantic schema to be inherited from by database schema."""

    id: int

    class Config:
        from_attributes = True
        model_exclude = {'id'}
