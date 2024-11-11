"""Base classes for all entities in the application."""

from __future__ import annotations

from typing import Annotated, Union

from ...data.schema import BaseModel, Meta, field


class Entity(BaseModel, kw_only=True):  # type: ignore[call-arg]
    """Abstract base class for all entities in the application.

    Entities are foundational data objects with an optional identifier and creation timestamp,
    accommodating new entities that have not yet been persisted.

    Attributes:
        uid (str): The unique identifier for the entity. None for new entities.
        created_at (Optional[datetime]): The timestamp of when the
        entity was created. None for new entities.
    """

    uid: Annotated[
        Union[str, int],
        Meta(title="Unique ID", description="The unique ID of the entity"),
    ] = field(default_factory=str)


class ValueObject(BaseModel, kw_only=True):  # type: ignore[call-arg]
    """Abstract base class for all value objects in the application.

    Value objects are immutable data objects that are used to describe entities.

    Value objects are immutable data objects that are used to describe entities.
    """

    pass
